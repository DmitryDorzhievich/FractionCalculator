import sys
from fractions import Fraction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPainter, QPixmap, QPen
from PyQt6.QtCore import Qt


# =========================
# вычисление дробей
# =========================

def parse_expression(expr):

    parts = expr.split()

    # ищем оператор
    for i, p in enumerate(parts):
        if p in ["+", "-", "*", ":"]:
            op = p
            left = " ".join(parts[:i])
            right = " ".join(parts[i+1:])
            return parse_number(left), op, parse_number(right)

    raise ValueError("оператор не найден")

def parse_number(text):
    """
    Преобразует текст в Fraction.
    Работает с:
    - целыми числами: 5
    - дробями: 3/4
    - смешанными: 1 2/3 или -1 2/3
    """
    text = text.strip()
    if not text:
        raise ValueError("Пустой текст")

    sign = 1
    if text[0] == "-":
        sign = -1
        text = text[1:].strip()

    # смешанное число
    if " " in text:
        whole, frac_part = text.split()
        whole = int(whole)
        num, den = map(int, frac_part.split("/"))
        return sign * Fraction(whole * den + num, den)

    # обычная дробь
    if "/" in text:
        num, den = map(int, text.split("/"))
        return sign * Fraction(num, den)

    # целое число
    return sign * Fraction(int(text))
    
def calculate(expr):

    try:

        a, op, b = parse_expression(expr)

        if op == "+":
            return a + b

        if op == "-":
            return a - b

        if op == "*":
            return a * b

        if op == ":":
            return a / b

    except:
        return None
    
def to_mixed(frac):
    if frac.numerator >= 0:
        whole = frac.numerator // frac.denominator
        remainder = frac.numerator % frac.denominator
    else:
        whole = -(abs(frac.numerator) // frac.denominator)
        remainder = abs(frac.numerator) % frac.denominator

    if remainder == 0:
        return whole, None

    return whole, Fraction(remainder, frac.denominator)

# =========================
# Canvas
# =========================

class Canvas(QWidget):

    def __init__(self):
        super().__init__()
        self.mixed = None

        self.expr = ""
        self.result = None

        # загрузка цифр
        self.digits = {}

        for i in range(15):
            self.digits[str(i)] = QPixmap(f"images/{i}.png")

    # установка выражения
    def set_expression(self, expr, result):

        self.expr = expr
        self.result = result

        if result:
            self.mixed = to_mixed(result)

        self.update()

    # рисование числа из картинок
    def draw_number(self, painter, number, x, y):

        number = str(number)

        offset = 0

        for d in number:

            if d == "-":
                pix = self.digits["12"]   # картинка минуса
            else:
                pix = self.digits[d]

            painter.drawPixmap(x + offset, y, pix)

            offset += pix.width()

    # рисование дроби
    def draw_fraction(self, painter, frac, x, y):

        num = frac.numerator
        den = frac.denominator

        num_len = len(str(num))
        den_len = len(str(den))

        line_len = max(num_len, den_len)

        num_start = (line_len - num_len)*18
        den_start = (line_len - den_len)*18
        
        # линия
        painter.drawLine(x, y + 53, x + 36*line_len, y + 53)

        # числитель
        self.draw_number(painter, num, x + num_start, y)

        # знаменатель
        self.draw_number(painter, den, x + den_start, y + 58)

        return line_len

    def draw_op(self, painter, op, x, y):
        if op == "+":
            pix = self.digits["11"]
            painter.drawPixmap(x, y, pix)
        elif op =="-":
            pix = self.digits["12"]
            painter.drawPixmap(x, y, pix)
        elif op == ":":
            pix = self.digits["14"]
            painter.drawPixmap(x, y, pix)
        elif op == "*":
            pix = self.digits["10"]
            painter.drawPixmap(x, y, pix)
        elif op == "=":
            pix = self.digits["13"]
            painter.drawPixmap(x, y, pix)

    def draw_mixed(self, painter, mixed, x, y):

        whole, frac = mixed

        offset = 0

        if whole != 0:
            self.draw_number(painter, whole, x, y + 40)
            offset = len(str(whole)) * 36 + 10

        if frac:
            self.draw_fraction(painter, frac, x + offset, y)

    # рисование канваса
    def paintEvent(self, event):

        if not self.expr:
            return

        painter = QPainter(self)

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(4)
        painter.setPen(pen)

        try:

            f1, op, f2 = parse_expression(self.expr)

            # первая дробь
            frac_0_len = self.draw_fraction(painter, f1, 40, 40) * 36

            # оператор
            self.draw_op(painter, op, frac_0_len + 5 + 40, 69)

            # вторая дробь
            frac_1_len = self.draw_fraction(painter, f2, frac_0_len + 46 + 40, 40) * 36

            # равно
            self.draw_op(painter, "=", frac_0_len + frac_1_len + 36 + 10 + 5 + 40, 69)

            # результат
            if self.result is not None:
                frac_res_len = self.draw_fraction(painter, self.result, frac_0_len + frac_1_len + 72 + 40 + 20, 40) * 36

            if self.mixed:

                # знак =
                self.draw_op(painter, "=", frac_0_len + frac_1_len + frac_res_len + 97 + 40, 69)

                # смешанный результат
                self.draw_mixed(painter, self.mixed, frac_0_len + frac_1_len + frac_res_len + 138 + 40, 40)

        except:
            pass


# =========================
# главное окно
# =========================

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор дробей")

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите выражение: 1/2 - 5/9")

        self.clear_button = QPushButton("C")
        self.clear_button.setFixedWidth(40)
        self.clear_button.setStyleSheet("font-size:18px")
        self.clear_button.setShortcut("Esc")

        input_layout.addWidget(self.input)
        input_layout.addWidget(self.clear_button)

        self.canvas = Canvas()

        layout.addLayout(input_layout)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.input.returnPressed.connect(self.calculate)
        self.clear_button.clicked.connect(self.clear)

    def calculate(self):

        expr = self.input.text()

        result = calculate(expr)

        self.canvas.set_expression(expr, result)

    def clear(self):

        self.input.clear()

        self.canvas.expr = ""
        self.canvas.result = None
        self.canvas.update()

# =========================
# запуск программы
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.resize(500, 250)
    window.show()

    sys.exit(app.exec())