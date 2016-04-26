import utils, visualize

def start(db, args):
    utils.checkNumberOfArgs(args, 0, True)
    if db.startTicket() == False:
        utils.panic("There already is an open work ticket.")
    visualize.openTickets(db)

def stop(db, args):
    notes = " ".join(args)
    if db.stopTicket(notes) == False:
        utils.panic("There is no open work ticket.")
    else:
        visualize.closedTickets(db, 1)

def log(db, args):
    if utils.checkNumberOfArgs(args, 0):
        visualize.closedTickets(db, -1)
    elif utils.checkNumberOfArgs(args, 1, True):
        if utils.checkIsInt(args[0]):
            visualize.closedTickets(db, int(args[0]))
        elif utils.checkIsStamp(args[0]):
            visualize.log(db, args[0])
        else:
            utils.panic("Argument '{}' is neither an integer nor a month "
                    "(format: MM/YYYY).".format(args[0]))

def sum(db, args):
    if utils.checkNumberOfArgs(args, 0):
        visualize.summary(db, utils.getCurrentStamp())
    elif utils.checkNumberOfArgs(args, 1, True):
        utils.checkIsStamp(args[0], True)
        visualize.summary(db, args[0])

def add(db, args):
    if len(args) < 3:
        utils.panic("Command requires at least 3 argument(s) "
                "({} given).".format(len(args)))
    utils.checkIsDate(args[0])
    utils.checkIsTime(args[1])
    utils.checkIsTime(args[2])
    notes = " ".join(args[3:])
    visualize.data(args[0], args[1], args[2], notes)
    print()
    if utils.question("Create the above work record?"):
        db.createEntry(args[0], args[1], args[2], notes)
        print("Done:")
        print()
        visualize.lastInserted(db)
        print()
    else:
        print("Aborted.")


def delete(db, args):
    utils.checkNumberOfArgs(args, 1, True)
    utils.checkIsInt(args[0], True)
    id = args[0]

    print()
    if visualize.ticket(db, id) == False:
        utils.panic("There is no ticket #{}.".format(id))
    print()
    if utils.question("Really delete above ticket #{}?".format(id), "no"):
        db.deleteEntry(id)
        print("Deleted ticket #{}.".format(id))
    else:
        print("Aborted.")
