from argparse import ArgumentParser
from csv import DictReader, DictWriter
import subprocess
from os import remove

"""
  Enter command line params and other stuff
"""


def cut_files(fname, fields):
    print 'Cutting {}...'.format(fname)
    pipe = subprocess.Popen(['cut', '-f', fields, fname],
                            stdout=subprocess.PIPE)
    with open('{}.cut'.format(fname[:fname.rfind('.')]), 'w') as f:
        f.writelines(pipe.stdout)


def dedup_files(base_name):
    print 'Deduping and minimizing {}...'.format(base_name)
    cut_name = '{}.cut'.format(base_name)
    min_name = '{}_minimized.csv'.format(base_name)
    with open(cut_name, 'r') as r, open(min_name, 'w') as w:
        reader = DictReader(r, delimiter='\t')
        writer = DictWriter(w, fieldnames=reader.fieldnames)
        writer.writeheader()
        file_data = set()
        for row in reader:
            row_data = tuple(row.values())
            if row_data not in file_data:
                file_data.add(row_data)
                writer.writerow(row)
    remove(cut_name)


def main():
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

    if args.all:
        from os import listdir
        files = [f for f in listdir('.') if f.endswith(('.txt', '.csv'))]
    else:
        files = args.files

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

    print files
    print fields

    for fname in files:
        cut_files(fname, fields)
        dedup_files(fname[:fname.rfind('.')])

if __name__ == '__main__':
    main()
