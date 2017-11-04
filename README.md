# Simple fast image converter

[http://schemaspy.org/](SchemaSpy)

[en]

Simple and high-speed image transformation using docker.

[jp]

dockerを使ってシンプルで高速な画像の画質調整を行う事ができます。

## Description

[en]

You can parallel computation with the core number of CPU's and can convert it faster than ImageMagick and Pillow by using Python Pillow-SIMD of high quality at high speed.

In addition, the environmental setting that is boring by trouble is unnecessary because this use Docker. You only start a container in any timing and can easily perform picture adjustment fast.

In addition, please warn the converted image because it is `overwritten`.

[jp]

CPUのコア数で並列処理をし、高速で高品質なPython Pillow-SIMDを使う事で、ImageMagickやPillowよりも、更に高速に変換する事ができます。

また、Dockerを使っているので、面倒で退屈な環境設定も不要です。任意のタイミングでコンテナを起動するだけで、簡単に高速に画質調整を行う事ができます。

尚、変換された画像は`上書きされる`ので、注意して下さい。

## Use cases

1. Jenkins git clone.
2. Set WORKSPACE environment. (WORKSPACE environment is automatically set by jenkins)
3. Execute Simple fast image converter. (docker-compose up)
4. Build application.
5. Deploy application.

## Features

- Docker v17
- docker-compose v1.16
- Alpine Linux v3.6
- Python v3.6.3
- Pillow-SIMD v4.3.0

## Requirement

- Docker(version 1.13.0 or higher)
- docker-compose
- image files

## Usage

```bash
# git clone
git clone https://github.com/treetips/simple-fast-image-converter.git
cd simple-fast-image-converter
# edit workspace path
export WORKSPACE=xxxxxxx
# Run containers and convert images
docker-compose up
```

## Change default image quality

[en]

`settings.txt` is the image configuration file.

When you change a picture of the default, set it as follows.

    DEFAULT_IMAGE_QUALITY=80

[jp]

`settings.txt` は画像設定ファイルです。

デフォルトの画質を変更する場合は以下のように設定して下さい。

    DEFAULT_IMAGE_QUALITY=80

## Change every image quality

[en]

When you change a picture every image format, set it as follows.

    JPEG=65
    GIF=70

The correspondence image format depends on Pillow-SIMD. Please confirm a correspondence format from the following.

http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html

[jp]

画像フォーマット毎に画質を変更する場合は以下のように設定して下さい。

    JPEG=65
    GIF=70

対応画像フォーマットはPillow-SIMDに依存しています。以下から対応フォーマットを確認して下さい。

http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html

## Change Lang

Edit docker-compose.yml.

    environment:
      - LANG=ja_JP.UTF-8

## Change timezone

Edit docker-compose.yml.

    environment:
      - TZ=Asia/Tokyo

## License

[MIT](http://b4b4r07.mit-license.org)