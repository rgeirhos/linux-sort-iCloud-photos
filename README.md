# linux-sort-iCloud-photos

## Description

If you'd like to download your iCloud photos to Linux and you thought they'd be sorted nicely, well, then you probably discovered that they have cryptic names (like `0a21e702-2ff6-4493-aeda-1a3ccc0b1829.jpg`) and don't contain any metadata according to which they can be sorted chronologically. At this point, you can either abandon the idea of downloading iCloud photos in a sorted fashion, or visit your closest Apple Store to buy a Mac, or - as the third and recommended option - you can follow the steps below to sort them chronologically on Linux. The core idea is to download them along with metadata, and then use a script to rename them with a `YYYY-MM-DD_Hour-Minute` prefix such that they appear in the correct chronological order.

## Steps

1. At https://privacy.apple.com/, log in and click on "Obtain a copy of your data". Select iCloud Photos and choose the desired file size (e.g. 2 GB). Complete request and download the data once you receive the notification email.
(Why not simply download the photos directly from iCloud photos? Unfortunately this approach will only get you the unsorted photos with a cryptic name but not the metadata - like dates - required for sorting them.)

2. Extract the `.zip` file(s) and locate the `Photos/` directory. Then, simply execute (for each of the extracted directories):

```bash
python3 sort_photos.py -d ./path/to/Photos/ --convert-HEIC-to-JPG
```

This will rename the photos using the metadata provided by Apple and thus afterwards the photos will be sorted by date. If you don't want your photos to be converted from `.HEIC` to `.JPG`, simply leave out the ``--convert-HEIC-to-JPG`` option.

## Requirements

Tested on Linux (Ubuntu 20.04 LTS) with Python3 using standard Python libraries (os, math, csv, tqdm, argparse).

If and only if you would like the script to convert `.HEIC` photos to `.JPG`, the `libheif-examples` library is required and can be installed as follows:

```bash
sudo apt install libheif-examples
```
