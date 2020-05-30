import re
import sympy
import cmath


def findnth(haystack, needle, n):
    cnt = -1
    for i in range(len(haystack)):
        if haystack[i] == needle:
            cnt += 1
            if cnt == n:
                return i
    return None


def first_order_equation(a, b):
    return -b/a


class MathSolver:
    def __init__(self):
        self.sin = r"sin\((.*)\)"
        self.cos = r"cos\((.*)\)"
        self.log = r"log\((.*)\)"
        self.power = r"([1-9][0-9]*)?x(\^[1-9][0-9]*)?"
        self.quadratic = r"(-?([1-9][0-9]*))?x\^2([+-]?([1-9][0-9]*)?x)?([+-]([1-9][0-9]*))?=0"
        self.first_order = r"(-?([1-9][0-9]*))?x([+-]([1-9][0-9]*))?=0"

    def outer_sign(self, s, sign_pos):
        open_parantheses = 0
        for i in range(sign_pos):
            if s[i] == '(':
                open_parantheses += 1
            elif s[i] == ')':
                open_parantheses -= 1
        if open_parantheses == 0:
            return True
        return False

    def break_plus(self, s):
        exp = s
        n = 0
        while findnth(exp, '+', n):
            pos = findnth(exp, '+', n)
            if self.outer_sign(exp, pos):
                return exp[:pos], exp[pos+1:]
            n += 1
        return None

    def break_multi(self, s):
        exp = s
        n = 0
        while findnth(exp, '*', n):
            pos = findnth(exp, '*', n)
            if self.outer_sign(exp, pos):
                return exp[:pos], exp[pos + 1:]
            n += 1
        return None

    def break_div(self, s):
        exp = s
        n = 0
        while findnth(exp, '/', n):
            pos = findnth(exp, '/', n)
            if self.outer_sign(exp, pos):
                return exp[:pos], exp[pos + 1:]
            n += 1
        return None

    def break_expression(self, s):
        rez = self.break_plus(s)
        if rez:
            return rez
        rez = self.break_multi(s)
        if rez:
            return rez
        rez = self.break_div(s)
        if rez:
            return rez
        return rez

    def derivative_single(self, exp):
        if exp == 'x':
            return ''
        r = re.search(self.sin, exp)
        if r:
            x = f"cos({r.group(1)})"
            if r.group(1) != 'x':
                x += f" * {self.derivative(r.group(1))}"
            return x
        r = re.search(self.cos, exp)
        if r:
            x = f"-sin({r.group(1)})"
            if r.group(1) != 'x':
                x += f" * {self.derivative(r.group(1))}"
            return x
        r = re.search(self.log, exp)
        if r:
            x = f"1/{r.group(1)}"
            if r.group(1) != 'x':
                x += f" * {self.derivative(r.group(1))}"
            return x
        r = re.search(self.power, exp)
        if r:
            a = 1
            b = 1
            if r.group(1):
                a = int(r.group(1))
            if r.group(2):
                b = int(r.group(2)[1:])
                return f"{a*b}x^{b-1}"
            else:
                return f"{a}"

    def derivative(self, exp):
        rez = self.break_plus(exp)
        if rez:
            return f"{self.derivative(rez[0])} + {self.derivative(rez[1])}"
        rez = self.break_multi(exp)
        if rez:
            return f"{self.derivative(rez[0])} * {rez[1]} + {rez[0]}*{self.derivative(rez[1])}"
        return self.derivative_single(exp)

    def quadratic_equation(self, a, b, c):
        d = b**2 - 4*a*c
        x1 = (-b-cmath.sqrt(d))/(2*a)
        x2 = (-b+cmath.sqrt(d))/(2*a)
        return x1, x2

    def parse_equation(self, equation):
        r = re.search(self.quadratic, equation)
        if r:
            a, b, c = 1, 0, 0
            if r.group(1):
                a = int(r.group(1))
            if r.group(3):
                b = int(r.group(3)[:-1])  # TODO: fix for '-' as input
            if r.group(5):
                c = int(r.group(5))
            x1, x2 = self.quadratic_equation(a, b, c)
            print(f"x1={x1}, x2={x2}")
        else:
            r = re.search(self.first_order, equation)
            if r:
                a, b = 1, 0
                if r.group(1):
                    a = int(r.group(1))
                if r.group(3):
                    b = int(r.group(3))
                print(f"x={first_order_equation(a, b)}")
            else:
                print("I don't understand the equation, please write it again.")


if __name__ == '__main__':
    solver = MathSolver()
    print(solver.parse_equation("sin(cos(x))"))
