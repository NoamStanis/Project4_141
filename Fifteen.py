import sys
import os
from random import shuffle
from time import sleep
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QWindow
from PyQt5.QtWidgets import QWidget, QApplication, QProgressBar, QLabel, QPushButton, QMainWindow

grid_size = 500
grid_coord = 50

window = None


class MainMenu(QWidget):
    def __init__(self, won):
        super().__init__()
        self.setWindowTitle('Main Menu')
        self.setGeometry(400, 250, 600, 600)

        self.title = QLabel("<font color='#199611'>15-Puzzle", self)
        self.title.setFont(QFont("Trebuchet MS", 70))
        self.title.setGeometry(90, 0, 450, 170)

        self.start = QPushButton("Play", self)
        self.setFont(QFont("Trebuchet MS", 20))
        self.start.setGeometry(150, 200, 300, 50)
        self.start.clicked.connect(self.play)

        self.exit = QPushButton("Exit", self)
        self.exit.setGeometry(150, 400, 300, 50)
        self.exit.clicked.connect(lambda x: sys.exit())

        self.show()

    def play(self):
        self.title.hide()
        self.start.hide()
        self.exit.hide()
        game = Fifteen()
        window.setCentralWidget(game)
        game.setParent(self)
        game.move(-10, -10)
        game.show()


class Fifteen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fifteen')
        self.setGeometry(400, 250, 600, 600)
        self.r_list = [[], [], [], []]
        self.moves = 0
        self.num_board = []
        self.solved = [[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 10, 11, 12],
                       [13, 14, 15, ' ']]
        self.board1 = []
        self.scramble()

        self.progress = QProgressBar(self)
        self.progress.setGeometry(250, 25, 100, 20)
        self.progress.setMaximum(16)
        self.progress.setTextVisible(False)
        self.progress.setAlignment(Qt.AlignRight)
        self.value = 0
        self.progress.setValue(self.value)

        self.percent = QLabel(str(self.progress.value() // 16) + "%", self)
        self.percent.setGeometry(360, 25, 100, 20)

        self.show()

    def scramble(self):
        """check if its solvable and if not recreate it"""
        possible = False
        while not possible:
            self.board1 = [i for i in range(1, 16)] + [' ']  # 1D List
            blank_spot = self.board1.index(' ')
            shuffle(self.board1)
            n = 4
            self.num_board = [self.board1[i:i + n] for i in
                              range(0, len(self.board1), n)]  # 2D version of the grid's list
            og_blank_spot = self.board1.index(' ')
            self.board1.remove(' ')
            for i in self.num_board:
                if ' ' in i:
                    blank_spot = 4 - self.num_board.index(i)

            inv = 0  # number of inversions
            for i in self.board1:
                for j in self.board1[self.board1.index(i):]:
                    if i > j:
                        inv += 1
            self.board1.insert(og_blank_spot, ' ')
            if blank_spot % 2 == 0 and inv % 2 != 0 or blank_spot % 2 != 0 and inv % 2 == 0:
                possible = True

    def paintEvent(self, event):
        qp = QPainter()
        grid_pen = QPen(Qt.black, 7)
        grid_brush = QBrush(QColor(56, 182, 199), Qt.SolidPattern)
        qp.begin(self)

        qp.setPen(grid_pen)
        qp.setBrush(grid_brush)

        if self.value < 6:
            for i in range(4):
                for j in range(4):
                    x = (i * 125) + 50
                    y = (j * 125) + 50
                    q = QRect(QPoint(x, y), QSize(125, 125))
                    self.r_list[i].append(q)

            qp.setFont(QFont("arial", 20))
            qp.drawText(50, 580, "Moves: " + str(self.moves))

            for i in range(len(self.r_list)):
                for j in range(4):
                    qp.drawRect(self.r_list[i][j])
                    qp.drawText(self.r_list[i][j], Qt.AlignCenter, str(self.num_board[j][i]))

        if self.value == 6:
            sleep(5)
            self.percent.hide()
            self.progress.hide()
            qp.setFont(QFont("Trebuchet MS", 90))
            qp.setPen(QPen(QColor(47, 100, 186), 7))
            qp.drawText(50, 300, "You Win!")

            self.value = 0
            self.main_button = QPushButton("Main Menu", self)
            self.main_button.setGeometry(150, 400, 300, 50)
            self.main_button.show()
            self.main_button.clicked.connect(lambda m: os.execl(sys.executable, sys.executable, *sys.argv))

        qp.end()

    def mousePressEvent(self, event):
        blank_pos = None
        x = event.x()
        y = event.y()
        row = (y - grid_coord) // 125
        col = (x - grid_coord) // 125
        mCoord = (row, col)  # The exact square which is clicked
        for r in self.num_board:
            for n in r:
                if n == ' ':
                    blank_pos = (self.num_board.index(r), r.index(n))  # position of the blank spot
        self.move_click(mCoord, blank_pos, self.num_board)

        completed_nums = []
        for n1 in range(len(self.num_board)):
            for n2 in range(4):
                if self.num_board[n1][n2] == self.solved[n1][n2] and self.num_board[n1][n2] not in completed_nums:
                    completed_nums.append(self.solved[n1][n2])
                    self.value = len(completed_nums)
                    self.progress.setValue(self.value)
                    self.percent.setText(str(self.value / 16 * 100) + "%")

        self.update()

    def move_click(self, mouse, blank, board):
        """
        Sees how far away the mouse click is from the blank, and move the numbers accordingly.
        :param mouse: Coordinates of the mouse click on the grid, tuple
        :param blank: Coordinates of the blank spot on the grid, tuple
        :param board: 2D list of all the numbers on screen, list
        :return: None
        """

        if mouse[0] == blank[0] and mouse[1] != blank[1]:  # Checks rows
            distance = mouse[1] - blank[1]
            d = abs(distance)
            if d == 1:
                clicked_num = board[mouse[0]][mouse[1]]
                board[blank[0]][blank[1]] = clicked_num
                board[mouse[0]][mouse[1]] = ' '
                self.moves += 1

            elif distance == -2:
                board[mouse[0]][mouse[1] + d] = board[mouse[0]][mouse[1] + d - 1]
                board[mouse[0]][mouse[1] + d - 1] = board[mouse[0]][mouse[1]]
                board[mouse[0]][mouse[1]] = ' '
                self.moves += d

            elif distance == -3:
                closest_num = board[mouse[0]][mouse[1] + d - 1]
                second_num = board[mouse[0]][mouse[1] + d - 2]
                board[blank[0]][blank[1]] = closest_num
                board[mouse[0]][mouse[1] + d - 1] = second_num
                board[mouse[0]][mouse[1] + d - 2] = board[mouse[0]][mouse[1]]
                board[mouse[0]][mouse[1]] = ' '

            elif distance == 2:
                board[mouse[0]][mouse[1] - distance] = board[mouse[0]][mouse[1] - distance + 1]
                board[mouse[0]][mouse[1] - distance + 1] = board[mouse[0]][mouse[1]]
                board[mouse[0]][mouse[1]] = ' '

            elif distance == 3:
                closest_num = board[mouse[0]][mouse[1] - distance + 1]
                second_num = board[mouse[0]][mouse[1] - distance + 2]
                board[blank[0]][blank[1]] = closest_num
                board[mouse[0]][mouse[1] - distance + 1] = second_num
                board[mouse[0]][mouse[1] - distance + 2] = board[mouse[0]][mouse[1]]
                board[mouse[0]][mouse[1]] = ' '

        if mouse[1] == blank[1] and mouse[0] != blank[0]:  # Checks columns
            distance = mouse[0] - blank[0]

            if abs(distance) == 1:
                clicked_num = board[mouse[0]][blank[1]]
                board[blank[0]][blank[1]] = clicked_num
                board[mouse[0]][mouse[1]] = ' '
                self.moves += 1

            elif distance == -2:
                d = abs(distance)
                board[mouse[0] + d][mouse[1]] = board[mouse[0] + d - 1][mouse[1]]
                board[mouse[0] + d - 1][mouse[1]] = board[mouse[0] + d - 2][mouse[1]]
                board[mouse[0] + d - 2][mouse[1]] = ' '
                self.moves += d

            elif distance == -3:
                d = abs(distance)
                closest_num = board[mouse[0] + d - 1][mouse[1]]
                second_num = board[mouse[0] + d - 2][mouse[1]]
                board[blank[0]][blank[1]] = closest_num
                board[mouse[0] + d - 1][mouse[1]] = second_num
                board[mouse[0] + d - 2][mouse[1]] = board[mouse[0] + d - 3][mouse[1]]
                board[mouse[0]][mouse[1]] = ' '
                self.moves += d

            elif distance == 2:
                board[mouse[0] - distance][mouse[1]] = board[mouse[0] - distance + 1][mouse[1]]
                board[mouse[0] - distance + 1][mouse[1]] = board[mouse[0] - distance + 2][mouse[1]]
                board[mouse[0] - distance + 2][mouse[1]] = ' '
                self.moves += distance

            elif distance == 3:
                closest_num = board[mouse[0] - distance + 1][mouse[1]]
                second_num = board[mouse[0] - distance + 2][mouse[1]]
                board[blank[0]][blank[1]] = closest_num
                board[mouse[0] - distance + 1][mouse[1]] = second_num
                board[mouse[0] - distance + 2][mouse[1]] = board[mouse[0] - distance + 3][mouse[1]]
                board[mouse[0]][mouse[1]] = ' '
                self.moves += distance


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = MainMenu(False)
    sys.exit(app.exec_())
