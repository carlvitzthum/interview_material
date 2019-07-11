import csv
import os
from contextlib import contextmanager

class ArithmeticDatabase(object):
    """
    A simple database backed by a csv file to contain arithmetic operations
    with two integers
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

    @contextmanager
    def open_read(self):
        csv_file = open(self.filepath, mode='r', newline='')
        yield csv.reader(csv_file, delimiter=',')

    def validate(self, row):
        """
        Validate the everything about the given row is correct.
        
        TODO: enough validation cases?

        Args:
            row (list): list of elements to write in the row

        Returns:
            bool: validation status
        """
        if row[0] not in self.operators:
            return False
        return True

    def write(self, row, validate=True, read_first=True):
        """
        Write the given row to the csv. Can optionally validate the row using
        the `self.validate` method

        Args:
            row (list): list of elements to write in the row
            validate (bool): whether to validate the row. Default False
            read_first (bool): if True, read the existing contents of the file
                to include in the write. Set to False on initial write

        Raises:
            Exception: if validation fails
        """
        if validate and not self.validate(row):
            raise Exception('Cannot write row as it fails validation: %s' % row)

        # writerow overwrites the entire csv. must read in prior contents
        if read_first:
            all_rows = self.read_all()
        else:
            all_rows = []
        all_rows.append(row)

        with self.open_write() as csv_file:
            csv_file.writerows(all_rows)

    def read_all(self):
        """
        Read all rows from the csv file and return them

        Returns:
            list: all rows from the file
        """
        with self.open_read() as csv_file:
            all_rows = [row for row in csv_file]
        return all_rows

    def readRow(self, row_idx):
        """
        Read and return row in the csv of index given by row_idx

        Args:
            row_idx (int): index of row to read in file
        """
        found = False
        all_rows = self.read_all()
        csv_file = self.open_read()
        for idx in csv_file:
            if row_idx == csv_file.line_num:
                found = True
        if not Found:
            raise Exception('Cannot read row idx %s since it exceeds length of the csv' % row_idx)
        return all_rows[row_idx]

    def print_all(self):
        """
        Print all rows in the csv
        """
        with self.open_read() as csv_file:
            for row in csv_file:
                print(row)

    def get_lines_with_answer(self, answer):
        """
        Return a list of all rows in the csv that have given answer
        """
        raise NotImplementedError
