from math_solver import MathSolver
from text_solver import TextPredictor
from termcolor import colored
import re


def main():
    predictor = TextPredictor()
    solver = MathSolver()

    print(colored("Hi, I'm your virtual teacher. What can I help you with?", 'green'))
    question = ''
    while question.lower() != 'thanks':
        question = input()

        m = re.match(r'i have a question about a (paragraph|passage)', question.lower())
        if m:
            print(colored(f'What {m.group(1)} do you have questions about?', 'green'))
            paragraph = input()
            print(colored(f'What question do you have about this {m.group(1)}?', 'green'))
            question = input()

            d = {'passage': paragraph, 'question': question}
            print(colored(predictor.predict(d), 'green'))
            continue

        m1 = re.match(r'i have a math problem', question.lower())
        m2 = re.match(r'i have a question about a math problem', question.lower())
        if m1 or m2:
            if m1:
                print(colored('What problem do you have?', 'green'))
            if m2:
                print(colored('What question do you have?', 'green'))

            while True:
                question = input()
                m = re.match(r'what is the derivative of (.*)\?', question.lower())
                if m:
                    print(colored(f'The derivative is: {solver.derivative(m.group(1))}', 'green'))
                    break
                m = re.match(r'find the derivative for (.*)', question.lower())
                if m:
                    print(colored(f'The derivative is: {solver.derivative(m.group(1))}', 'green'))
                    break

                m = re.match(r'what are the solutions for (.*)\?', question.lower())
                if m:
                    print(colored(f'The solutions are: {solver.solve(m.group(1))}', 'green'))
                    break
                m = re.match(r'find the solutions for (.*)', question.lower())
                if m:
                    print(colored(f'The solutions are: {solver.solve(m.group(1))}', 'green'))
                    break
                print(colored("I didn't quite get that, can you please reformulate?", 'green'))

    print(colored("You're welcome. Have a nice day!", 'green'))


if __name__ == '__main__':
    main()
