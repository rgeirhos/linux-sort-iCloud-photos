# linux-sort-iCloud-photos

## Description

## Steps

1. At https://privacy.apple.com/, log in and click on "Obtain a copy of your data". Select iCloud Photos and choose the desired file size (e.g. 2 GB). Complete request and download the data once you receive the notification email.
(Why not simply download the photos directly from iCloud photos? Unfortunately this approach will only get you the unsorted photos with a cryptic name but not the metadata - like dates - required for sorting them.)

2. Extract the `.zip` file(s) and locate the `Photos/` directory. Then, simply execute (for each of the extracted directories):

```bash
python3 sort_photos.py -d ./path/to/Photos/ --convert-HEIC-to-JPG
```

This will rename the photos using the metadata provided by Apple and thus afterwards the photos will be sorted by date. If you don't want your photos to be converted from `.HEIC` to `.JPG`, simply leave out the ``--convert-HEIC-to-JPG`` option.

## Requirements

Tested on Linux (Ubuntu 20.04 LTS) with Python3 using standard Python libraries (os, math, csv, tqdm).

If and only if you would like the script to convert `.HEIC` photos to `.JPG`, the `libheif-examples` library is required and can be installed as follows:

```bash
sudo apt install libheif-examples
```
