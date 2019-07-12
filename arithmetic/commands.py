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

    Raises:
        KeyError if the operator is invalid
    """
    operators = {
        'add': lambda a, b: a + b,
        'subtract': lambda a, b: a - b,
        'multiply': lambda a, b: a * b,
        'divide': lambda: a, b: a / b
    }
    try:
        return operators[operator](a,b)
    except:
        valid_keys = ', '.join(operators.keys())
        err_msg = 'Operator %s is not valid! Must be one of: %s' % (operator, valid_keys)
        raise KeyError(err_msg)


def write_arithmetic(filename, operator, a, b):
    """
    Write a single arithmetic operation to a ArithmeticDatabase backed by a
    csv file with the given filename
    """
    answer = do_arithmetic(operator, a, b)
    db = ArithmeticDatabase(filename, use_existing=True)
    db.write([operator, a, b, answer])
    db.print_all()


def write_multiplication_table(filename):
    """
    Write a large multiplication table to a ArithmeticDatabase backed by a
    csv file with the given filename. Use a buffer.
    """
    db = ArithmeticDatabase(filename, use_existing=True)
    for a in range(1, 10000):
        for b in range(1, 10000):
            answer = do_arithmetic('multiply', a, b)
            db.buffered_write(['multiply', a, b, answer])
    db.print_all()
