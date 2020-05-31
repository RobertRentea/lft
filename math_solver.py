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


def quadratic_equation(a, b, c):
    d = b**2 - 4*a*c
    x1 = (-b-cmath.sqrt(d))/(2*a)
    x2 = (-b+cmath.sqrt(d))/(2*a)
    return x1, x2


def redundant_paranthesis(exp):
    if exp[0] != '(' or exp[-1] != ')':
        return False

    count = 0
    for i in range(len(exp) - 1):
        if exp[i] == '(':
            count += 1
        elif exp[i] == ')':
            count -= 1

        if count == 0:
            return False
    if count == 1:
        return True
    return False


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
            return '1'
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
        if redundant_paranthesis(exp):
            exp = exp[1:-1]
        rez = self.break_plus(exp)
        if rez:
            a = self.derivative(rez[0])
            b = self.derivative(rez[1])
            if b.startswith('-'):
                return f"{a}{b}"
            else:
                return f"{a}+{b}"
        rez = self.break_multi(exp)
        if rez:
            return f"{self.derivative(rez[0])}*{rez[1]} + {rez[0]}*{self.derivative(rez[1])}"
        rez = self.break_div(exp)
        if rez:
            if rez[0] == '1':
                return f"(-1/{rez[1]}^2)*({self.derivative(rez[1])})"
            else:
                return f"-(({self.derivative(rez[0])})/{rez[1]}^2)*({self.derivative(rez[1])})"
        return self.derivative_single(exp)

    def solve(self, equation):
        r = re.search(self.quadratic, equation)
        if r:
            a, b, c = 1, 0, 0
            if r.group(1):
                a = int(r.group(1))
            if r.group(3):
                n = r.group(3)[:-1]
                if n == '-':
                    b = -1
                elif n == '+':
                    b = 1
                else:
                    b = int(r.group(3)[:-1])
            if r.group(5):
                c = int(r.group(5))
            x1, x2 = quadratic_equation(a, b, c)
            return f"x1={x1}, x2={x2}"
        else:
            r = re.search(self.first_order, equation)
            if r:
                a, b = 1, 0
                if r.group(1):
                    a = int(r.group(1))
                if r.group(3):
                    b = int(r.group(3))
                return f"x={first_order_equation(a, b)}"


if __name__ == '__main__':
    solver = MathSolver()
    print(solver.solve("sin(cos(x))"))
