import argparse
from commands import write_arithmetic


def main():
    """
    Main function for use on the command line. Write a single function to a
    ArithmeticDatabase backed by a csv file with given filename
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='filepath to write to')
    parser.add_argument('operator', help='arithmetic operator')
    parser.add_argument('number1', help='first number')
    parser.add_argument('number2', help='second number')

    args = parser.parse_args()
    write_arithmetic(args.infile, args.operator, int(args.number1), int(args.number2))


if __name__ == '__main__':
    main()
