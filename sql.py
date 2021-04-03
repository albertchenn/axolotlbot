# sql.py
# program that holds all the sql commands for axo bot
class SQL():
    def __init__(self, cursor, database):
        self.cursor = cursor
        self.lvls = database
        
    def checkExist(self, item):
            self.cursor.execute(f"SELECT * FROM levels")
            db = self.cursor.fetchall()
            for user in db:
                if user[0] == item:
                    return True
            return False
        
    def getXP(self, id):
        id = int(id)
        self.cursor.execute(f"SELECT * FROM levels WHERE id = '{id}'")
        row = self.cursor.fetchall()
        return int(row[0][2])

    def getLevel(self, id):
        id = int(id)
        self.cursor.execute(f"SELECT * FROM levels WHERE id = '{id}'")
        row = self.cursor.fetchall()
        return int(row[0][1])

    def editXP(self, id, amount):
        id = int(id)
        xpAdd = self.getXP(id) + amount

        self.cursor.execute(f"UPDATE levels SET xp = '{xpAdd}' WHERE id = '{id}' ")
        
        self.lvls.commit()

    def editLevel(self, id, amount):
        id = int(id)
        levelAdd = self.getLevel(id) + amount

        self.cursor.execute(f"UPDATE levels SET level = '{levelAdd}' WHERE id = '{id}' ")

        self.lvls.commit()

    def getIDs(self):
        self.cursor.execute(f"SELECT id FROM levels")

        column = self.cursor.fetchall()

        ids = [id[0] for id in column]

        return ids