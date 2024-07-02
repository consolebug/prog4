import mysql.connector
import random
import time
from highscores import HighScores

class Lingo:
    def __init__(self):
        start_time = time.time()
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="prog4"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT dutch_word FROM words')
        rows = self.cursor.fetchall()
        self.conn.close()
        if rows:
            self.woord = random.choice(rows)[0]
        else:
            self.woord = "taart"
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Lingo initialization time: {elapsed_time} seconds")

    def validate_input(self, input_word):
        start_time = time.time()
        all_correct = True
        result = ""
        used_letters = set()
        for i in range(len(self.woord)):
            if input_word[i] == self.woord[i]:
                result += f"<span style='color:green'>{input_word[i]}</span>"
            elif input_word[i] in self.woord and input_word[i] not in used_letters:
                result += f"<span style='color:yellow'>{input_word[i]}</span>"
                used_letters.add(input_word[i])
                all_correct = False
            else:
                result += f"<span style='color:red'>{input_word[i]}</span>"
                all_correct = False
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"validate_input execution time: {elapsed_time} seconds")
        return result, all_correct
