#!/usr/bin/env python
from argparse import ArgumentParser
from csv import DictReader, DictWriter
from os import remove
import subprocess

"""
This script is useful for shrinking and deduping large files. Many of the
  strategies were initially developed to make voter file data more manageable
  since most csv readers are not very efficient when processing data greater
  than a few GBs. The UNIX 'cut' command efficiently cuts down
  tab-delimited files to a more manageable size of only the fields the user
  wants. After that, the script uses Python's csv DictReader/Writer to place
  tuples of every row into a set to dedupe the data write it out to a minimized
  file.

Requirements:
    Python 2.7

File Assumptions:
    - if multiple files are processed, they all have the same format
    - the initial files are all tab-delimited and have column headers
    - if all directory files are to be processed, they have a .csv or .txt
        extension

"""


def cut_files(fname, fields):
    """Call UNIX 'cut' command and cut it down to only listed fields

    Keyword arguments:
    fname -- initial file name
    fields -- fields to cut the file down to

    """
    print 'Cutting {}...'.format(fname)
    pipe = subprocess.Popen(['cut', '-f', fields, fname],
                            stdout=subprocess.PIPE)
    # Write the cut file to file with the same name with the .cut extension
    with open('{}.cut'.format(fname[:fname.rfind('.')]), 'w') as f:
        f.writelines(pipe.stdout)


def dedup_files(base_name):
    """Using the base name of the file (extension not necessary because we no
    longer need that file) dedup the .cut file into a '_minimized.csv' file and
    remove the temporary .cut file

    Keyword arguments:
    base_name -- name of the intial file without extension information

    """
    print 'Deduping and minimizing {}...'.format(base_name)
    cut_name = '{}.cut'.format(base_name)
    min_name = '{}_minimized.csv'.format(base_name)
    with open(cut_name, 'r') as r, open(min_name, 'w') as w:
        reader = DictReader(r, delimiter='\t')
        writer = DictWriter(w, fieldnames=reader.fieldnames)
        writer.writeheader()
        # This set and row values tuple used to dedupe rows
        file_data = set()
        for row in reader:
            row_data = tuple(row.values())
            if row_data not in file_data:
                file_data.add(row_data)
                writer.writerow(row)
    # Remove the '.cut' file, was only used for temporary storage
    remove(cut_name)


def main():
    """Accepts command line arguments for files to process, cut and dedup each
    file based on listed fields

    Command line arguments:
    -f -- list of files to process
    -o -- numerical list of fields to keep and dedupe on
          ***IMPORTANT*** field list is 1, not 0 indexed
    -a -- flag to process all files in directory with .csv or .txt extension

    """
    usage = 'Dedupes large tab-delimited files based on given fields'
    description = """Accepts a list of files, uses UNIX \'cut\' command to
                        to minimize the files, and then dedupes data based
                        on remaining fields"""
    parser = ArgumentParser(usage=usage, description=description)
    parser.add_argument('-f', action='store', dest='files', nargs='*',
                        default=None, help='Space delimited list of files')
    parser.add_argument('-a', action='store_true', dest='all', default=False,
                        help='Flag to process all .csv/.txt directory files')
    parser.add_argument('-o', action='store', dest='fields', nargs='*',
                        default=None, help='Space delimited list of fields')

    args = parser.parse_args()

    # if -a flag is used, grab a list of all .txt and .csv files
    if args.all:
        from os import listdir
        files = [f for f in listdir('.') if f.endswith(('.txt', '.csv'))]
    else:
        files = args.files

    # if no field list is provided, print field list and request field
    #   numbers from user
    # ***IMPORTANT*** Field list is 1 and not 0 indexed
    if not args.fields:
        fieldnames = []
        with open(files[0], 'r') as r:
            reader = DictReader(r, delimiter='\t')
            fieldnames = reader.fieldnames
        for i, field_name in enumerate(fieldnames, start=1):
            print '{}. {}'.format(i, field_name)
        fields = raw_input('Comma delimited field #\'s to group by:')
    else:
        fields = ','.join(args.fields)

    # cut and dedup files in order
    for fname in files:
        cut_files(fname, fields)
        dedup_files(fname[:fname.rfind('.')])

if __name__ == '__main__':
    main()
