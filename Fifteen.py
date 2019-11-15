import sys
from random import shuffle
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QProgressBar, QLabel

grid_size = 500
grid_coord = 50


class Fifteen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fifteen')
        self.setGeometry(400, 250, 600, 600)
        self.r_list = [[], [], [], []]
        self.moves = 0
        self.num_board = []
        self.solved = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, ' ']]
        self.scramble()

        self.progress = QProgressBar(self)
        self.progress.setGeometry(250, 25, 100, 20)
        self.progress.setMaximum(16)
        self.progress.setTextVisible(True)
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
            self.num_board = [self.board1[i:i + n] for i in range(0, len(self.board1), n)]  # 2D version of the grid's list
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
        grid_pen = QPen(QPen(Qt.black, 7))
        grid_brush = QBrush(QColor(56, 182, 199), Qt.SolidPattern)
        qp.begin(self)

        qp.setPen(grid_pen)
        qp.setBrush(grid_brush)

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

        qp.end()

    def mousePressEvent(self, event):
        blank_pos = None
        board = self.num_board
        x = event.x()
        y = event.y()
        mPoint = QPoint(x, y)
        row = (y - grid_coord) // 125
        col = (x - grid_coord) // 125
        mCoord = (row, col)

        for r in board:
            for n in r:
                if n == ' ':
                    blank_pos = (board.index(r), r.index(n))  # position of the blank spot

        blank_above = (blank_pos[0] - 1, blank_pos[1])
        blank_below = (blank_pos[0] + 1, blank_pos[1])
        blank_left = (blank_pos[0], blank_pos[1] - 1)
        blank_right = (blank_pos[0], blank_pos[1] + 1)

        if (mCoord == blank_above and 0 <= mCoord[0] <= 3 and 0 <= mCoord[1] <= 3
                or mCoord == blank_below and 0 <= mCoord[0] <= 3 and 0 <= mCoord[1] <= 3
                or mCoord == blank_left and 0 <= mCoord[0] <= 3 and 0 <= mCoord[1] <= 3
                or mCoord == blank_right and 0 <= mCoord[0] <= 3 and 0 <= mCoord[1] <= 3):
            num = board[mCoord[0]][mCoord[1]]
            blankspot = board[blank_pos[0]][blank_pos[1]]
            board[blank_pos[0]][blank_pos[1]] = num
            board[mCoord[0]][mCoord[1]] = blankspot
            self.moves += 1

            completed_nums = []
            for n1 in range(len(self.num_board)):
                for n2 in range(4):
                    if self.num_board[n1][n2] == self.solved[n1][n2] and self.num_board[n1][n2] not in completed_nums:
                        completed_nums.append(self.solved[n1][n2])
                        self.value = len(completed_nums)
                        self.progress.setValue(self.value)
                        self.percent.setText(str(self.value / 16 * 100) + "%")

        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fifteen()
    sys.exit(app.exec_())
