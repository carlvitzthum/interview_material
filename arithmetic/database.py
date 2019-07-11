import csv
import os
from contextlib import contextmanager

class ArithmeticDatabase(object):
    """
    A simple database backed by a csv file to contain arithmetic operations
    with two integers and the corresponding answers
    """
    headers = ['operator', 'int1', 'int2', 'answer']
    operators = ['add', 'subtract', 'multiply', 'divide']

    def __init__(self, filepath, use_existing=False):
        """
        Initialize the csv file used as the basis for the database. Also write
        the headers to the file

        Args:
            filepath (str): path for the csv file
            use_existing (bool): if True, initialize with an existing file

        Raises:
            Exception: if not `use_existing` and a file with `filepath` exists
        """
        self.filepath = filepath
        if os.path.exists(filepath):
            if not use_existing:
                raise Exception('Cannot initialize ArithmeticDatabase; file %s already exists' % filepath)
        else:
            self.write(self.headers)

    @contextmanager
    def open_write(self):
        """
        Use a contextmanager to yield the csv.writer object

        Yields:
            csv.writer() object
        """
        csv_file = open(self.filepath, mode='w', newline='')
        yield csv.writer(csv_file, delimiter=',')
        csv_file.close()

    def write(self, row):
        """
        Write the given row to the csv

        Args:
            row (list): list of elements to write in the row
        """
        with self.open_write() as csv_file:
            csv_file.writerows([row])

    def print_all(self):
        """
        Print all rows in the csv
        """
        with self.open_read() as csv_file:
            for row in csv_file:
                print(row)
