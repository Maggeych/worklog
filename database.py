import sqlite3

class Work:

    def __init__(self, dbFile, name):
        self.connection = sqlite3.connect(dbFile)
        self.c = self.connection.cursor()
        self.name = name

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def query(self, qry, args = list()):
        self.c.execute(qry, args)
        return self.c.fetchall()

    def exists(self):
        self.c.execute(
            "SELECT name "
            "FROM sqlite_master "
            "WHERE type='table' AND "
            "name=?"
            , (self.name, ))
        return len(self.c.fetchall()) > 0

    def create(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS ? "
            "("
                "id integer primary key,"
                "startTime DATETIME NOT NULL,"
                "stopTime DATETIME,"
                "description TEXT"
            ")"
            , (self.name, ))

    def startTicket(self):
        self.c.execute(
            "SELECT datetime(startTime, 'localtime') "
            "FROM {} "
            "WHERE stopTime IS NULL".format(self.tableName()))
        if len(self.c.fetchall()) > 0:
            return False
        self.c.execute(
            "INSERT INTO {} (startTime) "
            "VALUES (datetime())"
            .format(self.tableName()))
        return True

    def stopTicket(self, notes):
        self.c.execute(
            "SELECT * "
            "FROM {} "
            "WHERE stopTime IS NULL"
            .format(self.tableName()))
        if len(self.c.fetchall()) == 0:
            return False
        self.c.execute(
            "UPDATE {} "
            "SET stopTime=datetime(), description=? "
            "WHERE id=("
                "SELECT id "
                "FROM {} "
                "WHERE stopTime IS NULL "
                "ORDER BY startTime ASC "
                "LIMIT 1"
            ")".format(self.tableName(), self.tableName())
            , (notes, ))
        return True

    def deleteEntry(self, id):
        self.c.execute(
            "DELETE "
            "FROM {} "
            "WHERE id=?".format(self.tableName())
            , (id, ))

    def tableName(self):
        return ''.join(chr for chr in self.name if chr.isalnum())
