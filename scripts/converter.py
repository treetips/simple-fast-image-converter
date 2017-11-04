# -*- coding:utf-8 -*-
"""
特定の拡張子の画像をPythonのPillow-SIMDで画像変換するモジュールです。
https://github.com/uploadcare/pillow-simd
"""
import platform
import os
import imghdr
import time
import multiprocessing
from typing import Any, List
from logging import basicConfig, getLogger, INFO
from PIL import Image

basicConfig(level=INFO, format="%(asctime)s %(levelname)-5s %(message)s")
log = getLogger(__name__)

# 変換対象にする拡張子
#（pngやgif等の可逆圧縮は処理が遅い割に圧縮率が非常に低いので、jpg等の非可逆圧縮のみを対象にする事をおすすめします）
SUPPORT_EXTENSIONS = os.getenv("SUPPORT_EXTENSIONS", ".jpg,.jpeg").split(",")
# dockerへのCPU割当数 = 並列処理の同時実行数
DOCKER_CPU_COUNT = multiprocessing.cpu_count()
# docker内での画像変換対象パス（docker-composeで指定）
SRC_PATH = "/images"

log.info("=== SYSTEM INFO =========================================")
log.info("System          : %s", platform.system())
log.info("Release         : %s", platform.release())
log.info("Version         : %s", platform.version())
log.info("Machine         : %s", platform.machine())
log.info("Processor       : %s", platform.processor())
log.info("Python version  : %s", platform.python_version())
log.info("Compiler        : %s", platform.python_compiler())
log.info("Docker cpu core : %d", DOCKER_CPU_COUNT)
log.info("=========================================================")

def get_image_file_path(base_file_path: str) -> List[str]:
    """
    始点ディレクトリから再帰的に画像ファイルを探す
    """
    file_paths: List[str] = []
    for (root, _, files) in os.walk(base_file_path):
        for file in files:
            file_path: str = os.path.join(root, file)
            # 対応拡張子以外はスキップ
            _, ext = os.path.splitext(file)
            if not ext in SUPPORT_EXTENSIONS:
                continue
            # 拡張子偽装も含め、対象が画像ファイルで無ければスキップ
            if imghdr.what(file_path) == None:
                continue
            file_paths.append(file_path)
    return file_paths

def split_src_path(src_file_paths: List[str]) -> List[List[str]]:
    """
    ファイルパスをCPUのコア数の要素数単位で分割する
    """
    return [src_file_paths[i:i + DOCKER_CPU_COUNT]
            for i in range(0, len(src_file_paths), DOCKER_CPU_COUNT)]

def get_image_quality(image_format: str) -> int:
    """
    圧縮品質を取得する http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html
    settings.txtのkey=valueに「フォーマット名=品質」の形式で設定することで、
    フォーマット毎に品質値を変更する事ができます。
    settings.txtに、JPGE=70 等のユーザ指定の値が有れば使い、無ければユーザ指定のデフォルト値を使い、
    それでも無ければシステムデフォルトの値を使用する。
    """
    return int(os.getenv(image_format, os.getenv("DEFAULT_IMAGE_QUALITY", "70")))

def convert(file_paths: List[str]):
    """
    画像変換を実行する
    """
    for src_file_path in file_paths:
        start: float = time.time()

        # 対象ファイルから拡張子を取得
        _, ext = os.path.splitext(src_file_path)
        dest_file_path: str = src_file_path
        # 画像フォーマット等の設定
        image: Image = Image.open(src_file_path, "r")
        image_format: int = image.format
        compress_quality: int = get_image_quality(image_format)
        try:
            # 拡張子偽装(.pngなのに中身がjpg等)の場合は、本当の拡張子で変換する
            # （例）.pngだが中身はjpgの場合、jpgとして変換し、拡張子はそのまま.pngで保存する
            image.save(dest_file_path, image_format, quality=compress_quality, optimize=True)
        except:
            import traceback
            log.error('%s : %s : %s', image_format, dest_file_path, traceback.format_exc())

        elapsed_time: float = time.time() - start
        log.info(str("ext={0}, format={1}, quality={2}, time={3:.2f}s, path={4}".format(
            ext, image_format, compress_quality, elapsed_time, dest_file_path)))

def convert_parallel(src_file_path_units: List[List[str]]):
    """
    画像変換を並列実行する
    """
    jobs = []
    for path_unit in src_file_path_units:
        job: Any = multiprocessing.Process(target=convert, args=(path_unit, ))
        jobs.append(job)
        job.start()
    # 全てのジョブの完了を待つ
    [job.join() for job in jobs]

if __name__ == "__main__":
    start: float = time.time()

    # 変換対象ファイルパスリスト
    src_file_paths: List[str] = get_image_file_path(SRC_PATH)
    # 並列処理するためにCPUコア数枚に配列を分割
    src_file_path_units: List[List[str]] = split_src_path(src_file_paths)
    # 並列画像変換実行
    convert_parallel(src_file_path_units)

    elapsed_time: float = time.time() - start
    log.info(f'elapsed_time = ' + str("{0:.2f}".format(elapsed_time)) + 's')
