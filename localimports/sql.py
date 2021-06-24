# sql.py
# program that holds all the sql commands for axo bot
class SQL():
    def __init__(self, cursor, database):
        self.cursor = cursor
        self.lvls = database
        
    def checkExist(self, id):
            self.cursor.execute(f"SELECT * FROM levels WHERE id = {id}")
            db = self.cursor.fetchall()

            return db
        
    def getXP(self, id):
        id = int(id)
        self.cursor.execute(f"SELECT * FROM levels WHERE id = {id}")
        row = self.cursor.fetchall()
        return int(row[0][2])

    def getLevel(self, id):
        id = int(id)
        self.cursor.execute(f"SELECT * FROM levels WHERE id = {id}")
        row = self.cursor.fetchall()
        return int(row[0][1])

    def editXP(self, id, amount):
        id = int(id)
        xpAdd = self.getXP(id) + amount

        self.cursor.execute(f"UPDATE levels SET xp = {xpAdd} WHERE id = {id} ")
        
        self.lvls.commit()

    def editLevel(self, id, amount):
        id = int(id)
        levelAdd = self.getLevel(id) + amount

        self.cursor.execute(f"UPDATE levels SET level = {levelAdd} WHERE id = {id} ")

        self.lvls.commit()

    def getIDs(self):
        self.cursor.execute(f"SELECT id FROM levels")

        column = self.cursor.fetchall()

        ids = [id[0] for id in column]

        return ids
    
    def addNewUser(self):
        self.cursor.execute(f"INSERT INTO levels VALUES ({id}, 1, 1)")
        self.lvls.commit()