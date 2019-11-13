import sys
from random import shuffle
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QApplication

grid_size = 500
grid_coord = 50


class Fifteen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fifteen')
        self.setGeometry(400, 250, 600, 600)
        self.r_list = [[], [], [], []]
        self.moves = 0
        self.scramble()
        self.show()

    def scramble(self):
        """check if its solvable and if not recreate it"""
        possible = False
        while not possible:
            board1 = [i for i in range(1, 16)] + [' ']  # 1D List
            blank_spot = board1.index(' ')
            shuffle(board1)
            n = 4
            self.num_board = [board1[i:i + n] for i in range(0, len(board1), n)]  # 2D version of the grid's list
            board1.remove(' ')
            inv = 0  # number of inversions
            for i in board1:
                for j in board1[board1.index(i):]:
                    if i > j:
                        inv += 1
            board1.insert(blank_spot, ' ')
            if (blank_spot // 2) % 2 == 0 and inv % 2 != 0 or (blank_spot // 2) % 2 != 0 and inv % 2 == 0:
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
        row = (event.y() - grid_coord) // 125
        col = (event.x() - grid_coord) // 125
        if 0 <= row <= 3 and 0 <= col <= 3:
            self.moves += 1
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fifteen()
    sys.exit(app.exec_())
