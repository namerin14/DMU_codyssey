import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setGeometry(100, 100, 360, 540)
        self.setStyleSheet('background-color: black;')
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.display.setStyleSheet('font-size: 52px; background: black; color: white; border: none;')
        self.display.setFixedHeight(int(self.height() * 0.3))
        vbox.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, row_values in enumerate(buttons):
            for col, value in enumerate(row_values):
                button = QPushButton(value)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setMinimumHeight(70)
                button.setStyleSheet(self.get_button_style(value))
                button.clicked.connect(lambda _, val=value: self.on_click(val))

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

    def get_button_style(self, text):
        base_style = 'border-radius: 35px; min-width: 70px; min-height: 70px;'
        if text in ['÷', '×', '-', '+', '=']:
            return f'background-color: orange; color: white; font-size: 40px;  {base_style}'
        elif text in ['AC', '+/-', '%']:
            return f'background-color: gray; color: white; font-size: 30px; {base_style}'
        else:
            return f'background-color: #333333; color: white; font-size: 30px; {base_style}'

    def on_click(self, value):
        if value == 'AC':
            self.display.clear()
        elif value == '+/-':
            current_text = self.display.text()
            if current_text:
                if current_text.startswith('-'):
                    self.display.setText(current_text[1:])
                else:
                    self.display.setText('-' + current_text)
        elif value == '=':
            try:
                expression = self.display.text()
                expression = expression.replace('÷', '/').replace('×', '*')
                result = eval(expression)
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
