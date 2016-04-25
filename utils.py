import sys, os, errno, re

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
    print()
    help()
    sys.exit(2)

def checkNumberOfArgs(args, length, panicOnFalse = False):
    if len(args) != length:
        if panicOnFalse:
            panic("Command requires {} argument(s) ({} given).".format(
                length, len(args)
                ))
        return False
    return True

def checkIsInt(obj, panicOnFalse = False):
    try:
        ret = int(obj)
    except ValueError:
        if panicOnFalse:
            panic("Given argument '{}' is expected to be an integer.".format(obj))
        return False
    return True

def checkIsStamp(s, panicOnFalse = False):
    stampPattern = re.compile("^(0[0-9]|1[0-2])/[0-9][0-9][0-9][0-9]$")
    if stampPattern.match(s) == None:
        if panicOnFalse:
            panic("{} is not a valid stamp. Use 'MM/YYYY'.".format(s))
        return False
    return True

def checkIsDate(s):
    datePattern = re.compile("^([0-2][0-9]|3[0-1]).(0[1-9]|1[0-2]).[0-9][0-9][0-9][0-9]$")
    if datePattern.match(s) == None:
        panic("{} is not a valid stamp. Use 'DD.MM.YYYY'.".format(s))
    
def checkIsTime(s):
    timePattern = re.compile("^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
    if timePattern.match(s) == None:
        panic("{} is not a valid time. Use 'HH:MM'.".format(s))

def prepareFolder(name):
    folderExpanded = os.path.expanduser(name)
    try:
        os.makedirs(folderExpanded)
    except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(folderExpanded):
                pass
            else:
                raise
    return folderExpanded
