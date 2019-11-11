import sys

from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QLabel

grid_size = 500
grid_coord = 50


class Fifteen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fifteen')
        self.setGeometry(400, 250, 600, 600)
        self.board = [[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12],
                      [13, 14, 15, -1]]
        self.g_list = [[], [], [], []]

        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        grid_pen = QPen(QPen(Qt.black, 7))
        grid_brush = QBrush(QColor(56, 182, 199), Qt.SolidPattern)
        qp.begin(self)

        qp.setPen(grid_pen)
        qp.setBrush(grid_brush)
        # qp.drawRect(grid_coord, grid_coord, grid_size, grid_size)

        # for i in range(1, 4):  # draw the grid
        #     x = (i * 125) + 50
        #     qp.drawLine(x, 50, x, 550)
        #     qp.drawLine(50, x, 550, x)

        for i in range(4):
            for j in range(4):
                x = (i * 125) + 50
                y = (j * 125) + 50
                q = QRect(QPoint(x, y), QSize(125, 125))
                self.g_list[i].append(q)

        for item in self.g_list:
            for i in range(4):
                qp.drawRect(item[i])

    def mousePressEvent(self, event):
        row = (event.y() - grid_coord) // 125
        col = (event.x() - grid_coord) // 125
        print(row, col)

        # for i in range(4):
        #     for j in range(4):
        #         x = (i * 125) + 62.5
        #         y = (j * 125) + 62.5
        #         print(x, y)

        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fifteen()
    sys.exit(app.exec_())