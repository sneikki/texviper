import sys

def main(args):
    if '--cli' in args[1:]:
        print("Running cli")
    else:
        print("Running gui")

if __name__ == '__main__':
    main(sys.argv)
