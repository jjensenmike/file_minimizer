from argparse import ArgumentParser

"""
  Enter command line params and other stuff
"""


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
                        default=None, help='Space delimite list of fields')

    args = parser.parse_args()

    if args.all:
        from os import listdir
        files = [f for f in listdir('.') if f.endswith(('.txt', '.csv'))]
    else:
        files = args.files

    if not args.fields:
        print 'Get fields'
    else:
        fields = args.fields

    print files
    print fields

if __name__ == '__main__':
    main()
