# sql.py
# program that holds all the sql commands for axo bot
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ["TOKEN"]  # taking environment variables from .env
PASSWORD = os.environ["PASSWORD"]
USER = os.environ["USR"]
HOST = os.environ["HOST"]
DATABASE = os.environ["DATABASE"]
PORT = os.environ["PORT"]

class SQL():
    def __init__(self):
        self.lvls = mysql.connector.connect(user = USER,
                                            password = PASSWORD,
                                            host = HOST,
                                            port = PORT,
                                            database = DATABASE)

        self.cursor = self.lvls.cursor()
    
    def checkExist(self, item):
        self.cursor.execute(f"SELECT * FROM levels")
        db = self.cursor.fetchall()
        for user in db:
            if user[0] == item:
                return True
        return False 

    def getXP(self, id):
        self.cursor.execute(f"SELECT * FROM levels WHERE id = '{id}'")
        row = self.cursor.fetchall()
        return int(row[0][2])

    def getLevel(self, id):
        self.cursor.execute(f"SELECT * FROM levels WHERE id = '{id}'")
        row = self.cursor.fetchall()
        return int(row[0][1])

    def editXP(self, id, amount):
        xpAdd = self.getXP(id) + amount

        self.cursor.execute(f"UPDATE levels SET xp = '{xpAdd}' WHERE id = '{id}' ")
        
        self.lvls.commit()

    def editLevel(self, id, amount):
        levelAdd = self.getLevel(id) + amount

        self.cursor.execute(f"UPDATE levels SET level = '{levelAdd}' WHERE id = '{id}' ")

        self.lvls.commit()

    def getIDs(self):
        self.cursor.execute(f"SELECT id FROM levels")

        column = self.cursor.fetchall()

        ids = [id[0] for id in column]

        return ids