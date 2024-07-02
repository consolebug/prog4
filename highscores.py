import mysql.connector
from datetime import datetime

class HighScores:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="prog4"
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS highscores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                score INT NOT NULL,
                date DATE NOT NULL
            )
        ''')
        self.conn.commit()

    def add_highscore(self, name, score):
        date = datetime.now().date()
        self.cursor.execute('''
            INSERT INTO highscores (name, score, date)
            VALUES (%s, %s, %s)
        ''', (name, score, date))
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()