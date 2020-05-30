from math_solver import MathSolver
from text_solver import TextPredictor
from termcolor import colored


def main():
    predictor = TextPredictor()
    solver = MathSolver()
    print(colored("Hi, I'm your virtual teacher. What can I help you with?", 'green'))
    question = ''
    while question != 'exit':
        question = input()

        if question.lower() == 'i have a question about a paragraph':
            print(colored('What paragraph do you have questions about?', 'green'))
            paragraph = input()
            print(colored('What question do you have about this paragraph?', 'green'))
            question = input()

            d = {'passage': paragraph, 'question': question}
            print(predictor.predict(d))


if __name__ == '__main__':
    main()
