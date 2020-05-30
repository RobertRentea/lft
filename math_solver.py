import re
import sympy
import cmath

expression = "sin(cos(x))"
sin = r"sin\((.*)\)"
cos = r"cos\((.*)\)"
log = r"log\((.*)\)"
power = r"([1-9][0-9]*)?x(\^[1-9][0-9]*)?"
quadratic = r"(-?([1-9][0-9]*))?x\^2([+-]?([1-9][0-9]*)?x)?([+-]([1-9][0-9]*))?=0"
first_order = r"(-?([1-9][0-9]*))?x([+-]([1-9][0-9]*))?=0"


def outer_sign(s, sign_pos):
    open_parantheses = 0
    for i in range(sign_pos):
        if s[i] == '(':
            open_parantheses += 1
        elif s[i] == ')':
            open_parantheses -= 1
    if open_parantheses == 0:
        return True
    return False


def findnth(haystack, needle, n):
    cnt = -1
    for i in range(len(haystack)):
        if haystack[i] == needle:
            cnt += 1
            if cnt == n:
                return i
    return None


def break_plus(s):
    exp = s
    n = 0
    while findnth(exp, '+', n):
        pos = findnth(exp, '+', n)
        if outer_sign(exp, pos):
            return exp[:pos], exp[pos+1:]
        n += 1
    return None


def break_multi(s):
    exp = s
    n = 0
    while findnth(exp, '*', n):
        pos = findnth(exp, '*', n)
        if outer_sign(exp, pos):
            return exp[:pos], exp[pos + 1:]
        n += 1
    return None


def break_div(s):
    exp = s
    n = 0
    while findnth(exp, '/', n):
        pos = findnth(exp, '/', n)
        if outer_sign(exp, pos):
            return exp[:pos], exp[pos + 1:]
        n += 1
    return None


def break_expression(s):
    rez = break_plus(s)
    if rez:
        return rez
    rez = break_multi(s)
    if rez:
        return rez
    rez = break_div(s)
    if rez:
        return rez
    return rez


def derivative_single(exp):
    if exp == 'x':
        return ''
    r = re.search(sin, exp)
    if r:
        x = f"cos({r.group(1)})"
        if r.group(1) != 'x':
            x += f" * {derivative(r.group(1))}"
        return x
    r = re.search(cos, exp)
    if r:
        x = f"-sin({r.group(1)})"
        if r.group(1) != 'x':
            x += f" * {derivative(r.group(1))}"
        return x
    r = re.search(log, exp)
    if r:
        x = f"1/{r.group(1)}"
        if r.group(1) != 'x':
            x += f" * {derivative(r.group(1))}"
        return x
    r = re.search(power, exp)
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


def derivative(exp):
    rez = break_plus(exp)
    if rez:
        return f"{derivative(rez[0])} + {derivative(rez[1])}"
    rez = break_multi(exp)
    if rez:
        return f"{derivative(rez[0])} * {rez[1]} + {rez[0]}*{derivative(rez[1])}"
    return derivative_single(exp)


def quadratic_equation(a, b, c):
    d = b**2 - 4*a*c
    x1 = (-b-cmath.sqrt(d))/(2*a)
    x2 = (-b+cmath.sqrt(d))/(2*a)
    return x1, x2


def first_order_equation(a, b):
    return -b/a


def parse_equation(equation):
    r = re.search(quadratic, equation)
    if r:
        a, b, c = 1, 0, 0
        if r.group(1):
            a = int(r.group(1))
        if r.group(3):
            b = int(r.group(3)[:-1])  # TODO: fix for '-' as input
        if r.group(5):
            c = int(r.group(5))
        x1, x2 = quadratic_equation(a, b, c)
        print(f"x1={x1}, x2={x2}")
    else:
        r = re.search(first_order, equation)
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
    parse_equation(input())
