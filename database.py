import sqlite3, utils

class WorkTable:

    def __init__(self, dbCursor, name):
        self.c = dbCursor
        self.name = ''.join(chr for chr in name if chr.isalnum())
        self.overviewName = self.name + "_overview"
        self.openName = self.name + "_open"
        # Create the table and views if they don't exist yet.
        if not self.tableExists(self.name):
            if not utils.question("There is no work named '{}'. Create it?".format(name), "no"):
                utils.panic("Invalid work name.")
        self.createIfNotExists()

    def overview(self, limit):
        if limit < 0:
            qry = "SELECT id, date, start, stop, duration, stamp, description " \
                "FROM {}"
            self.c.execute(qry.format(self.overviewName))
        else:
            qry = "SELECT id, date, start, stop, duration, stamp, description " \
                "FROM (" \
                "SELECT * FROM {} ORDER BY date DESC LIMIT ?" \
                ") sub " \
                "ORDER BY date ASC"
            self.c.execute(qry.format(self.overviewName), (limit, ))
        return self.c.fetchall()

    def openTickets(self):
        self.c.execute(
            "SELECT id, date, start, durationClock, durationDecimal "
            "FROM {}"
            .format(self.openName))
        return self.c.fetchall()

    def ticket(self, id):
        self.c.execute(
            "SELECT id, date, start, stop, duration, stamp, description "
            "FROM {} "
            "WHERE id=?"
            .format(self.overviewName), (id, ))
        return self.c.fetchone()

    def lastInserted(self):
        self.c.execute(
            "SELECT id, date, start, stop, duration, stamp, description "
            "FROM {} "
            "WHERE id=last_insert_rowid()"
            .format(self.overviewName))
        return self.c.fetchone()

    def matchingStamp(self, stamp):
        self.c.execute(
            "SELECT id, date, start, stop, duration, stamp, description "
            "FROM {} "
            "WHERE stamp=?"
            .format(self.overviewName), (stamp, ))
        return self.c.fetchall()

    def stampSum(self, stamp):
        self.c.execute(
            "SELECT sum(duration) "
            "FROM {} "
            "WHERE stamp=?"
            .format(self.overviewName), (stamp, ))
        sumResult = self.c.fetchone()
        if sumResult[0] == None:
            return 0.0
        return sumResult[0]


    def startTicket(self):
        if len(self.openTickets()) > 0:
            return False
        self.c.execute(
            "INSERT INTO {} (startTime) "
            "VALUES (datetime())"
            .format(self.name))
        return True

    def stopTicket(self, notes):
        tickets = self.openTickets()
        if len(tickets) == 0:
            return False
        self.c.execute(
            "UPDATE {} "
            "SET stopTime=datetime(), description=? "
            "WHERE id=?"
            .format(self.name, self.name), (notes, tickets[0][0]))
        return True

    def createEntry(self, date, startTime, stopTime, notes):
        dateSplit = date.split(".")
        dateStr = dateSplit[2] + "-" + dateSplit[1] + "-" + dateSplit[0]
        startStr = dateStr + " " + startTime
        stopStr = dateStr + " " + stopTime
        self.c.execute(
            "INSERT INTO {} (startTime, stopTime, description) "
            "VALUES (datetime(?, 'utc'), datetime(?, 'utc'), ?)"
            .format(self.name), (startStr, stopStr, notes))

    def deleteEntry(self, id):
        self.c.execute(
            "DELETE "
            "FROM {} "
            "WHERE id=?"
            .format(self.name), (id, ))

    def createIfNotExists(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS {} "
            "("
                "id integer primary key,"
                "startTime DATETIME NOT NULL,"
                "stopTime DATETIME,"
                "description TEXT"
            ")"
            .format(self.name))
        self.c.execute(
            "CREATE VIEW IF NOT EXISTS {} AS "
            "SELECT "
                "id, "
                "strftime('%d.%m.%Y', datetime(startTime, 'localtime')) AS date, "
                "strftime('%H:%M', datetime(startTime, 'localtime')) AS start, "
                "strftime('%H:%M', datetime(stopTime, 'localtime')) AS stop, "
                "(julianday(stopTime) - julianday(startTime))*24 AS duration, "
                "strftime('%m/%Y', datetime(startTime, 'localtime')) AS stamp, "
                "description "
            "FROM {} "
            "WHERE stopTime IS NOT NULL "
            "ORDER BY startTime ASC"
            .format(self.overviewName, self.name))
        self.c.execute(
            "CREATE VIEW IF NOT EXISTS {} AS "
            "SELECT "
                "id, "
                "strftime('%d.%m.%Y', datetime(startTime, 'localtime')) AS date, "
                "strftime('%H:%M', datetime(startTime, 'localtime')) AS start, "
                "printf('%02d:%02d', cast((julianday('now')-julianday(startTime))*24%60 as integer), "
                    "cast((julianday('now')-julianday(startTime))*24*60%60 as integer)) "
                    "AS durationClock, "
                "cast((julianday('now') - julianday(startTime))*24 as real) AS durationDecimal "
            "FROM {} "
            "WHERE stopTime IS NULL "
            "ORDER BY startTime DESC"
            .format(self.openName, self.name))

    def tableExists(self, name):
        self.c.execute("SELECT "
            "name "
            "FROM sqlite_master "
            "WHERE type='table' AND name=?"
            , (name, ))
        return len(self.c.fetchall()) > 0
