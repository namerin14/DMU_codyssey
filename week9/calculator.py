import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton,
    QVBoxLayout, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setGeometry(100, 100, 360, 540)
        self.setStyleSheet('background-color: black;')
        self.current_expression = ''  # 현재 수식 저장용
        self.initUI()  # UI 초기화

    def initUI(self):
        vbox = QVBoxLayout()

        # 결과 출력 화면 설정
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.display.setStyleSheet('font-size: 52px; background: black; color: white; border: none;')
        self.display.setFixedHeight(int(self.height() * 0.3))
        vbox.addWidget(self.display)

        # 버튼 배열 정의
        grid = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 생성 및 연결
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

    # 버튼 스타일 지정
    def get_button_style(self, text):
        base_style = 'border-radius: 35px; min-width: 70px; min-height: 70px;'
        if text in ['÷', '×', '-', '+', '=']:
            return f'background-color: orange; color: white; font-size: 40px; {base_style}'
        elif text in ['AC', '+/-', '%']:
            return f'background-color: gray; color: white; font-size: 30px; {base_style}'
        else:
            return f'background-color: #333333; color: white; font-size: 30px; {base_style}'

    # 버튼 클릭 처리
    def on_click(self, value):
        if value == 'AC':
            self.reset()  # 초기화 과제 반영
        elif value == '+/-':
            self.negative_positive()  # 음수/양수 변환 과제 반영
        elif value == '%':
            self.percent()  # 백분율 처리 과제 반영
        elif value == '=':
            self.equal()  # 결과 계산 과제 반영
        elif value in ['+', '-', '×', '÷']:
            self.current_expression += ' ' + value + ' '
            self.display.setText(self.current_expression)
        elif value == '.':
            if not self.current_expression or self.current_expression[-1] in ' +-×÷':
                self.current_expression += '0.'
            elif '.' not in self.current_expression.split()[-1]:
                self.current_expression += '.'
            self.display.setText(self.current_expression)  # 소수점 중복 입력 방지
        else:
            self.current_expression += value  # 숫자 누적 입력
            self.display.setText(self.current_expression)

    # 사칙연산 메소드
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    # 초기화 기능 구현
    def reset(self):
        self.current_expression = ''
        self.display.setText('')

    # 음수/양수 변환 기능 구현
    def negative_positive(self):
        try:
            tokens = self.current_expression.strip().split()
            if tokens and tokens[-1].replace('.', '', 1).lstrip('-').isdigit():
                last = tokens[-1]
                if last.startswith('-'):
                    tokens[-1] = last[1:]
                else:
                    tokens[-1] = '-' + last
                self.current_expression = ' '.join(tokens)
                self.display.setText(self.current_expression)
        except:
            self.display.setText('Error')

    # 백분율 기능 구현
    def percent(self):
        try:
            tokens = self.current_expression.strip().split()
            if tokens and tokens[-1].replace('.', '', 1).lstrip('-').isdigit():
                tokens[-1] = str(float(tokens[-1]) / 100)
                self.current_expression = ' '.join(tokens)
                self.display.setText(self.current_expression)
        except:
            self.display.setText('Error')

    # 결과 계산 및 예외 처리, 반올림, 폰트 조절
    def equal(self):
        try:
            tokens = self.current_expression.strip().split()
            if len(tokens) != 3:
                self.display.setText('Error')
                return

            a, op, b = tokens
            a = float(a)
            b = float(b)

            if op == '+':
                result = self.add(a, b)
            elif op == '-':
                result = self.subtract(a, b)
            elif op == '×':
                result = self.multiply(a, b)
            elif op == '÷':
                result = self.divide(a, b)
            else:
                self.display.setText('Error')
                return

            if isinstance(result, float):
                result = round(result, 6)  # 소수점 6자리 반올림

            self.current_expression = str(result)
            self.adjust_font_size(str(result))  # 폰트 크기 조절
            self.display.setText(str(result))

        except ZeroDivisionError:
            self.display.setText('Cannot divide by 0')  # 0 나누기 예외 처리
        except OverflowError:
            self.display.setText('Overflow')  # 숫자 범위 초과 처리
        except:
            self.display.setText('Error')

    # 결과 길이에 따른 폰트 크기 조정
    def adjust_font_size(self, text):
        length = len(str(text))
        if length <= 8:
            font_size = 52
        elif length <= 12:
            font_size = 40
        elif length <= 16:
            font_size = 30
        else:
            font_size = 20
        self.display.setStyleSheet(
            f'font-size: {font_size}px; background: black; color: white; border: none;'
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
