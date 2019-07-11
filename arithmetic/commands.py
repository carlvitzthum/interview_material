from database import ArithmeticDatabase


def do_arithmetic(operator, a, b):
    """
    Given string operator and two numbers a and b, perform the given
    arithmetic operation and return the answer

    Args:
        operator (string): arithmetic operator to perform
        a (int): first number
        b (int): second number

    Returns:
        int: value of answer
    """
    operators = {
        'add': a + b,
        'subtract': a - b,
        'multiply': a * b,
        'divide': a / b
    }
    return operators[operator]


def write_arithmetic(filename, operator, a, b):
    """
    Write a single arithmetic operation to a ArithmeticDatabase backed by a
    csv file with the given filename
    """
    answer = do_arithmetic(operator, a, b)
    db = ArithmeticDatabase(filename, use_existing=True)
    db.write([operator, a, b, answer])
    db.print_all()
