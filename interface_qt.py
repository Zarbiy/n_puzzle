import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

class PuzzleWindow(QWidget):
    def __init__(self, size, path, interval=500):
        super().__init__()
        self.size = size
        self.path = path
        self.index = 0
        self.interval = interval
        self.setWindowTitle(f"{size}x{size} Puzzle")
        self.setFixedSize(800, 800)

        self.cell_size = self.width() // size
        
        # init box for numbers
        self.labels = []
        for i in range(size):
            row = []
            for j in range(size):
                label = QLabel(self)
                label.setGeometry(j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(QFont("Arial", 30, QFont.Weight.Bold))
                label.setStyleSheet("border: 1px solid black;")
                row.append(label)
            self.labels.append(row)

        mid = size // 2
        self.button = QPushButton("Start", self)
        self.button.setFont(QFont("Arial", 16))
        self.button.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; border-radius: 10px;")
        self.button.setGeometry(
            mid*self.cell_size + self.cell_size//4,
            mid*self.cell_size + self.cell_size//4,
            self.cell_size//2,
            self.cell_size//2
        )
        self.button.clicked.connect(self.start_animation)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)

        # initial state
        self.update_grid(self.path[0])

    def update_grid(self, puzzle):
        for i in range(self.size):
            for j in range(self.size):
                value = puzzle[i*self.size + j]
                label = self.labels[i][j]
                label.setText(str(value) if value != 0 else "")
                if value == 0:
                    label.setStyleSheet("background-color: lightgray; border: 2px solid gray; border-radius: 10px;")
                else:
                    label.setStyleSheet("color: black; background-color: lightgreen; border: 2px solid black; border-radius: 10px;")

    def start_animation(self):
        self.button.hide()
        self.index = 0
        self.timer.start(self.interval)

    def next_step(self):
        self.index += 1
        if self.index >= len(self.path):
            self.timer.stop()
            return
        self.update_grid(self.path[self.index])


def show_game_qt(size, path):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = PuzzleWindow(size, path, 800)
    window.show()
    app.exec()
