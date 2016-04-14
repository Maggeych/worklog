import sys

def question(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def panic(msg):
    print("\033[1m{}\033[0m".format(msg))
    help()
    sys.exit(2)

def checkNumberOfArgs(argv, length):
    if len(argv) - 1 != length:
        panic("Command {} requires {} argument(s) ({} given).".format(
            argv[0], length, len(argv) - 1
            ))

def checkIsInt(obj):
    try:
        ret = int(obj)
    except ValueError:
        panic("Given argument '{}' is expected to be an integer.".format(obj))
