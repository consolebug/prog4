import sys
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QWidget, QMessageBox, QInputDialog)
from lingo import Lingo
from highscores import HighScores

class LingoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.lingo = Lingo()
        self.highscores = HighScores()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.start_time = time.time()
        self.timer.start(1000)
        self.remaining_guesses = 5
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lingo @ - Stijn van den Sool')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()

        self.label = QLabel('Voer hier een 5 letterig woord in:')
        self.layout.addWidget(self.label)

        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self.check_word)  
        self.layout.addWidget(self.input)

        self.result_label = QLabel('')
        self.result_label.setTextFormat(Qt.RichText)
        self.layout.addWidget(self.result_label)

        self.timer_label = QLabel('Verstreken tijd: 0 seconden')
        self.layout.addWidget(self.timer_label)

        self.button = QPushButton('Check Word', self)
        self.button.clicked.connect(self.check_word)
        self.layout.addWidget(self.button)

        self.highscores_button = QPushButton('View Highscores', self)
        self.highscores_button.clicked.connect(self.show_highscores)
        self.layout.addWidget(self.highscores_button)

        self.setLayout(self.layout)

    def check_word(self):
        if self.remaining_guesses == 0:
            return
        user_input = self.input.text()
        if len(user_input) == 5:
            result, all_correct = self.lingo.validate_input(user_input)
            current_text = self.result_label.text()
            self.result_label.setText(f'{current_text}<br>Resultaat: {result}')
            if all_correct:
                elapsed_time = time.time() - self.start_time
                print("Correct woord. Stopping timer and showing message box.")
                self.timer.stop()
                name, ok = QInputDialog.getText(self, 'Name Input', 'Voer uw naam in:')
                if ok:
                    self.highscores.add_highscore(name, int(elapsed_time)) 
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setText("Goed gedaan! Het woord was juist")
                msg_box.setWindowTitle("Gefeliciteerd")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                self.button.setEnabled(False)
            else:
                self.remaining_guesses -= 1
                print(f"Incorrect word guessed. {self.remaining_guesses} guesses remaining.")
                if self.remaining_guesses == 0:
                    print("No more guesses left.")
                    self.timer.stop()
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setText("Sorry, je hebt teveel geraden.")
                    msg_box.setWindowTitle("Game Over")
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()
        else:
            current_text = self.result_label.text()
            self.result_label.setText(f'{current_text}<br>Voer alleen een 5 letter woord in aub.')
        self.input.setText('')

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.timer_label.setText(f'Verstreken tijd: {int(elapsed_time)} seconden')

    def show_highscores(self):
        self.highscores.cursor.execute("SELECT name, score, date FROM highscores ORDER BY score ASC")
        rows = self.highscores.cursor.fetchall()
        highscores_text = "<h1>Highscores</h1><ol>"
        for row in rows:
            highscores_text += f"<li>{row[0]} - {row[1]} seconds - {row[2]}</li>"
        highscores_text += "</ol>"
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(highscores_text)
        msg_box.setWindowTitle("Highscores")
        msg_box.exec_()

    def closeEvent(self, event):
        self.highscores.close_connection()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lingo_app = LingoApp()
    lingo_app.show()
    sys.exit(app.exec_())