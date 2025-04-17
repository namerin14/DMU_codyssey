import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLineEdit


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setGeometry(100, 100, 300, 400)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet('font-size: 22px; height: 60px;')
        vbox.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, row_values in enumerate(buttons):
            for col, value in enumerate(row_values):
                button = QPushButton(value)
                button.setStyleSheet('font-size: 20px; padding: 20px;')
                button.clicked.connect(lambda _, val=value: self.on_click(val))

                # 0 버튼은 가로로 두 칸 차지
                if value == '0':
                    grid.addWidget(button, row + 1, 0, 1, 2)
                elif value == '.':
                    grid.addWidget(button, row + 1, 2)
                elif value == '=':
                    grid.addWidget(button, row + 1, 3)
                else:
                    grid.addWidget(button, row + 1, col)

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def on_click(self, value):
        if value == 'AC':
            self.display.clear()
        elif value == '=':
            try:
                result = eval(self.display.text())
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        else:
            self.display.setText(self.display.text() + value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
