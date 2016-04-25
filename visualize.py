import datetime, textwrap, math

# Print a list of all open tickets.
def openTickets(workTable):
    openTickets = workTable.openTickets()
    if len(openTickets) > 0:
        for ticket in (openTickets):
            print(       "━━━━━━━━━━━━━━━━━━━━━")
            print("\033[1m SINCE ┊ \033[0m{} [{:3.1f}]".format(ticket[3], ticket[4]))
            print("\033[1m  DATE ┊ \033[0m{}".format(ticket[1]))
            print("\033[1m  TIME ┊ \033[0m{}".format(ticket[2]))
            print(       "━━━━━━━━━━━━━━━━━━━━━")
        return True
    return False

# Print an overview of the latest <numberOfEntries> closed working tickets.
# If <numberOfEntries> is negative all tickets are printed.
def closedTickets(workTable, numberOfEntries):
    return printTicketList(workTable.overview(numberOfEntries))

# Print an overview of the month <stamp>.
def log(workTable, stamp):
    return printTicketList(workTable.matchingStamp(stamp))

# Print the summary for <month>.
def summary(workTable, stamp):
    matches = workTable.matchingStamp(stamp)
    s = workTable.stampSum(stamp)
    print(" ══════════════════════")
    for m in matches:
        print(" {}┊{}┊{}  \033[37m#{:0>3}\033[0m".format(m[1], m[2], m[3], m[0]))
    print(" ══════════════════════")
    print("   \033[1mSUM {}:\033[0m {:.2}".format(stamp, s))
    print(" ══════════════════════")

# Print ticket with given id.
def ticket(workTable, id):
    t = workTable.ticket(id)
    if t == None:
        return False
    printTicket(t)
    return True

# Print the last inserted ticket.
def lastInserted(workTable):
    t = workTable.lastInserted()
    if t == None:
        return False
    printTicket(t)
    return True

# Print given data instead of querying the database.
def data(date, startTime, stopTime, notes):
    print(       "━━━━━━━━━━━━━━━━━━━━━")
    print("\033[1m  DATE ┊ \033[0m{}".format(date))
    print("\033[1m START ┊ \033[0m{}".format(startTime))
    print("\033[1m  STOP ┊ \033[0m{}".format(stopTime))
    print(       "━━━━━━━━━━━━━━━━━━━━━")
    print("\033[1m NOTES\033[0m")
    if len(notes) == 0:
        print(" (none)")
    else:
        for l in textwrap.wrap(notes, 39):
            print(" {}".format(l))


# ------------------------------------------------------------------------------
# All printing is done here. Change these for a different look.

# Print the given list as closed tickets.
def printTicketList(lst):
    if len(lst) > 0:
        for entry in lst:
            print()
            printTicket(entry)
        print()
        return True
    return False

def printTicket(t):
    print(" \033[1m{}\033[0m  {} ↷ {}   {}  [#{:0>3}]".format(
        t[1], t[2], t[3], "{:3.1f}".format(t[4]), t[0]
        ))
    for l in textwrap.wrap(t[6], 39):
        print(" {}".format(l))
