#!/usr/bin/env python3

import csv
import os
import math
from tqdm import tqdm
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-d", "--directory", dest="directory",
                    help="directory path to /Photos/", metavar="DIR")
parser.add_argument("-c", "--convert-HEIC-to-JPG",
                    action="store_true", dest="convert_HEIC_to_JPG", default=False,
                    help="convert HEIC images to JPG")
args = parser.parse_args()


PHOTO_INDEX = {} # mapping from filename to Img object

TIME_IDX = 4
AM_PM_IDX = 5
DAY_IDX = 2
MONTH_IDX = 1
YEAR_IDX = 3

MONTH_DICT = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
    }

class Img():

    def __init__(self, img_name, date_string):

        self.img_name = img_name
        self.date_string = date_string
        self.hours, self.minutes = self.convert_time(date_string[TIME_IDX],
                                                     date_string[AM_PM_IDX])
        self.day = int(date_string[DAY_IDX])
        self.month = MONTH_DICT[date_string[MONTH_IDX]]
        self.year = int(date_string[YEAR_IDX])

        self.formatted_name = self.format_name()


    def convert_time(self, time, am_pm):

        time = float(time.replace(":", "."))
        if am_pm == "PM":
            time += 12.0

        minutes, hours = math.modf(time) 
        
        return int(hours), round(minutes*100)


    def format_name(self):

        return f"{self.year}-{self.month:02d}-{self.day:02d}_{self.hours:02d}-{self.minutes:02d}_{self.img_name}"


def build_photo_index(directory, csv_filename):

    csv_filepath = os.path.join(directory, csv_filename)
    assert os.path.exists(csv_filepath), f"no such file: {csv_filepath}"

    with open(csv_filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(reader) # skipping header
        for row in reader:
            r = ",".join(row)
            img_name = r.split(",")[0]
            date_string = r.split(",")[1:]

            img = Img(img_name = img_name, date_string = date_string)
            PHOTO_INDEX[img.img_name] = img.formatted_name


def build_index(directory):

    assert os.path.exists(directory), f"directory {directory} not found"
    assert os.path.isdir(directory), f"{directory} is not a directory"

    for f in sorted(os.listdir(directory)):
        if f.endswith(".csv"):
            print(f"Processing {f}")
            build_photo_index(directory = directory,
                              csv_filename = f) 


def sort_images(directory, convert_HEIC_to_JPG):

    file_list = sorted(os.listdir(directory))
    for f in tqdm(file_list):
        if not f.endswith(".csv"):
            if PHOTO_INDEX.get(f):
                new_filename = PHOTO_INDEX.get(f)
            elif PHOTO_INDEX.get(f.replace(".MOV", ".HEIC")):
                # for .MOV, use .HEIC metadata if no .MOV metadata is available
                new_filename = PHOTO_INDEX.get(f.replace(".MOV", ".HEIC")).replace(".HEIC", ".MOV")
            else:
                print(f"file {f}: no metadata found, thus keeping this file as is")
                continue

            old_filepath = os.path.join(directory, f)
            new_filepath = os.path.join(directory, new_filename)
            os.rename(old_filepath, new_filepath)

            if convert_HEIC_to_JPG and new_filename.endswith(".HEIC"):
                os.system(f"heif-convert -q 100 {new_filepath} {new_filepath.replace('.HEIC', '.JPG')} > /dev/null")
                os.remove(new_filepath)


if __name__ == "__main__":

    build_index(directory = args.directory)
    sort_images(directory = args.directory,
                convert_HEIC_to_JPG = args.convert_HEIC_to_JPG)
