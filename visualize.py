import datetime, textwrap, math

# Print a list of all open tickets.
def openTickets(c):
    openTickets = c.query(
        "SELECT id, datetime(startTime, 'localtime') "
        "FROM WorkingTime WHERE "
        "stopTime IS NULL "
        "ORDER BY startTime DESC"
        )
    if len(openTickets) > 0:
        for entry in (openTickets):
            printOpenTicket(entry[1])
        return True
    return False

# Print an overview of the latest <numberOfEntries> closed working tickets.
# If <numberOfEntries> is negative all tickets are printed.
def closedTickets(c, numberOfEntries=3):
    closedTickets = c.query(
        "SELECT "
        "id, datetime(startTime, 'localtime'), "
        "datetime(stopTime, 'localtime'), description "
        "FROM WorkingTime WHERE "
        "stopTime IS NOT NULL "
        "ORDER BY startTime DESC "
        "LIMIT ?"
        , (str(numberOfEntries), ))
    print()
    print("\033[1m{:^41}\033[0m".format("Latest {} working hours:".format(numberOfEntries)))
    return printTicketQuery(closedTickets)

# Print the overview of ticket #<id>.
def ticket(c, id):
    t = c.query(
        "SELECT id, datetime(startTime, 'localtime'), "
        "datetime(stopTime, 'localtime'), description "
        "FROM WorkingTime WHERE "
        "stopTime IS NOT NULL AND "
        "id=?"
        , (id, ))
    return printTicketQuery(t)

# Print the summary for <month>.
def summary(c, month):
    s = c.query(
        "SELECT id, datetime(startTime, 'localtime'), "
        "datetime(stopTime, 'localtime'), description "
        "FROM WorkingTime WHERE "
        "stopTime IS NOT NULL AND "
        "strftime('%m', startTime)=? "
        "ORDER BY startTime DESC"
        , ("{:02}".format(int(month)),))
    return printTicketQuery(s)

# ------------------------------------------------------------------------------
# All printing is done here. Change these for a different look.

# Print the given list as closed tickets.
def printTicketQuery(lst):
    if len(lst) > 0:
        for entry in lst:
            print("─────────────────────────────────────────")
            printClosedTicket(entry[0], entry[1], entry[2], entry[3])
        print("─────────────────────────────────────────")
        print()
        return True
    return False

def printOpenTicket(startTimeStr):
    startTime = datetime.datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()

    dateStr = datetime.datetime.strftime(startTime, '%d.%m.%Y')
    timeStr = datetime.datetime.strftime(startTime, '%H:%M')

    d = (now - startTime).total_seconds()
    h = math.floor(d / 3600)
    m = math.floor(d / 60) % 60
    d /= 3600

    print(       "━━━━━━━━━━━━━━━━━━━━━")
    print("\033[1m SINCE ┊ \033[0m{:02}:{:02} [{:3.1f}]".format(h, m, d))
    print("\033[1m  DATE ┊ \033[0m{}".format(dateStr))
    print("\033[1m  TIME ┊ \033[0m{}".format(timeStr))
    print(       "━━━━━━━━━━━━━━━━━━━━━")

def printClosedTicket(id, startTimeStr, stopTimeStr, description):
    startTime = datetime.datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S')
    stopTime = datetime.datetime.strptime(stopTimeStr, '%Y-%m-%d %H:%M:%S')

    dateStr = str(datetime.datetime.strftime(startTime, '%d.%m.%Y'))
    startStr = str(datetime.datetime.strftime(startTime, '%H:%M'))
    stopStr = str(datetime.datetime.strftime(stopTime, '%H:%M'))

    duration = (stopTime - startTime).total_seconds()
    hours = (duration / 3600)

    print(" \033[1m{}\033[0m  {} ↷ {}   {}  [#{:0>3}]".format(
        dateStr, startStr, stopStr, "{:3.1f}".format(hours), id
        ))
    for l in textwrap.wrap(description, 39):
        print(" {}".format(l))
