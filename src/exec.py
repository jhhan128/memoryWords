import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
from gtts import gTTS
from playsound import playsound
import os
import random
import threading
import platform


def pre_run():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    database_dir = os.path.join(current_dir, 'database.txt')
    result_dir = os.path.join(current_dir, 'result.txt')
    inf_dir = os.path.join(current_dir, 'inf.txt')

    ip2 = open(inf_dir, 'r')

    s = ip2.readline()
    s = ip2.readline()
    length = int(s)

    ip = open(database_dir, 'r')
    op = open(result_dir, 'w')

    arr = []

    while True:
        s = ip.readline()
        if not s: break
        arr.append(s)

    random.shuffle(arr)
    for i in range(min(len(arr), length)): op.write(arr[i])

    return result_dir


class WordQuizApp(QWidget):
    def __init__(self, filename):
        super().__init__()

        self.words = self.load_words(filename)
        self.total_questions = len(self.words)
        self.current_question = 0
        self.correct_answers = 0

        self.init_ui()

    def init_ui(self):
        self.question_label = QLabel(self)
        self.question_label.setFont(QFont("NanumBarunGothic", 30, QFont.Medium))  # Adjusted font size
        self.question_label.setAlignment(Qt.AlignCenter)

        self.choice_buttons = [QPushButton(self) for _ in range(4)]

        for button in self.choice_buttons:
            button.clicked.connect(self.check_answer)
            button.setFixedSize(300, 45)  # Adjusted button size (width: 200, height: 45)

        self.result_label = QLabel(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, self.total_questions)
        self.progress_info_label = QLabel(self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.question_label, 0, 0, 1, 2)  # Spanning two columns
        self.layout.setSpacing(10)  # Fixed spacing between all buttons
        self.layout.setContentsMargins(10, 10, 10, 10)  # Fixed margin around the buttons
        self.layout.setAlignment(Qt.AlignCenter)  # Center align the content

        # Add vertical spacing between question and buttons
        self.layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed), 1, 0)

        row, col = 2, 0  # Adjusted row to add spacing
        for button in self.choice_buttons:
            self.layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        self.layout.addWidget(self.result_label, row + 1, 0, 1, 2)  # Spanning two columns
        self.layout.addWidget(self.progress_bar, row + 2, 0, 1, 2)  # Spanning two columns
        self.layout.addWidget(self.progress_info_label, row + 3, 0, 1, 2)  # Spanning two columns

        self.setGeometry(300, 300, 600, 550)  # Adjusted window size
        self.setWindowTitle('memoryWords')

        self.show_next_question()
        self.show()

    def load_words(self, filename):
        words = []
        with open(filename, 'r') as file:
            for line in file:
                try: word, meaning = line.strip().split('|')
                except ValueError:
                    print(line)
                    sys.exit(1)
                words.append({'word': word, 'meaning': meaning})
        return words

    def show_next_question(self):
        if self.current_question < self.total_questions:
            word_data = self.words[self.current_question]
            word = word_data['word']
            correct_meaning = word_data['meaning']

            choices = [correct_meaning]
            while len(choices) < 4:
                random_word = random.choice(self.words)['meaning']
                if random_word not in choices:
                    choices.append(random_word)

            random.shuffle(choices)

            self.question_label.setText(f"{word}")
            self.progress_bar.setValue(self.current_question + 1)
            progress_info = f"{self.current_question+1}/{self.total_questions}"
            self.progress_info_label.setStyleSheet("color: Grey;")
            self.progress_info_label.setText(progress_info)

            # Use gTTS to generate speech from text
            threading.Thread(target=self.speak_word, args=(word,)).start()

            for i in range(4):
                self.choice_buttons[i].setText(choices[i])
                self.choice_buttons[i].setEnabled(True)
                self.choice_buttons[i].setStyleSheet("")

            self.result_label.clear()
        else:
            self.show_quiz_result()

            self.current_question = 0
            self.correct_answers = 0

        self.current_question += 1

    def speak_word(self, word):
        # Use gTTS to generate speech from text
        tts = gTTS(text=word, lang='en')
        tts.save("temp.mp3")

        # Play the generated speech using playsound
        playsound("temp.mp3")

        # Remove the temporary file
        os.remove("temp.mp3")

    def check_answer(self):
        sender = self.sender()
        selected_meaning = sender.text()
        correct_meaning = self.words[self.current_question - 1]['meaning']

        for button in self.choice_buttons:
            button.setEnabled(False)

        if selected_meaning == correct_meaning:
            sender.setStyleSheet("background-color: #66FF66; color: #000000;")
            self.correct_answers += 1
        else:
            sender.setStyleSheet("background-color: #FF6666; color: #000000;")
            for button in self.choice_buttons:
                if button.text() == correct_meaning:
                    button.setStyleSheet("background-color: #66FF66; color: #000000;")

        QTimer.singleShot(1500, self.show_next_question)  # Reduced timeout to 2 seconds

    def show_feedback(self, title, message):
        self.result_label.setText(f"{title}: {message}")

    def show_quiz_result(self):
        # Remove original elements
        self.question_label.clear()
        for button in self.choice_buttons:
            button.deleteLater()
        self.result_label.deleteLater()
        self.progress_bar.deleteLater()
        self.progress_info_label.deleteLater()

        # Add the result message label
        result_message = f"{self.correct_answers} / {self.total_questions} ({round(100*(self.correct_answers/self.total_questions))})"
        final_result_label = QLabel(self)
        final_result_label.setFont(QFont("NanumBarunGothic", 36, QFont.Medium))
        final_result_label.setAlignment(Qt.AlignCenter)
        final_result_label.setText(result_message)
        final_result_label.setStyleSheet("color: White;")
        self.layout.addWidget(final_result_label, 0, 0, 1, 2, Qt.AlignCenter)


if __name__ == '__main__':
    result_dir = pre_run()
    app = QApplication(sys.argv)
    ex = WordQuizApp(result_dir)
    sys.exit(app.exec_())