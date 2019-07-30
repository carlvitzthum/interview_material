import csv
import os
from contextlib import contextmanager


class ArithmeticDatabase(object):
    """
    A simple database backed by a csv file to contain arithmetic operations
    with two integers and the corresponding answer
    """
    headers = ['operator', 'int1', 'int2', 'answer']
    valid_operators = ['add', 'subtract', 'multiply', 'divide']
    buffer_size = 1024

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
                return Exception('Cannot initialize ArithmeticDatabase; file %s already exists' % filepath)
        else:
            self.write(self.headers)

    @contextmanager
    def open_write(self):
        """
        Use a contextmanager to yield the csv.writer object

        Yields:
            csv.writer() object
        """
        csv_file = open(self.filepath, mode='a', newline='')
        yield csv.writer(csv_file, delimiter=',')
        csv_file.close()

    @contextmanager
    def open_read(self):
        """
        Use a contextmanager to yield the csv.reader object

        Yields:
            csv.writer() object
        """
        csv_file = open(self.filepath, mode='r+', newline='')
        yield csv.reader(csv_file, delimiter=',')

    def validate(self, row):
        """
        Validate the everything about the given row is correct.

        Args:
            row (list): list of elements to write in the row

        Returns:
            bool: validation status
        """
        if row[0] not in self.valid_operators:
            return False
        return True

    def write(self, row, validate=True):
        """
        Write the given row to the csv. Can optionally validate the row using
        the `self.validate` method

        Args:
            row (list): list of elements to write in the row
            validate (bool): whether to validate the row. Default False

        Raises:
            Exception: if validation fails
        """
        if validate and not self.validate(row):
            raise Exception('Cannot write row as it fails validation: %s' % row)

        with self.open_write() as csv_file:
            csv_file.writerow(row)

    def buffered_write(self, row, validate=True):
        """
        Use a buffer to improve performance of writing. Leverage `csv.writerows`
        to write the entire buffer at once

        Args:
            row (list): list of elements to write in the row
            validate (bool): whether to validate the row. Default False

        Raises:
            Exception: if validation fails
        """
        buffer = []
        if validate and not self.validate(row):
            raise Exception('Cannot write row as it fails validation: %s' % row)

        buffer.append(row)
        if len(buffer) >= self.buffer_size:
            with self.open_write() as csv_file:
                csv_file.writerows(buffer)
            # clean up the buffer
            del buffer

    def write_entire_buffer_mp(self, validate=True):
        """
        Write all rows from the aforementioned buffer above using
        multiprocessing for some sweet performance increases!

        Args:
            validate (bool): whether to validate the row. Default False

        Raises:
            Exception: if validation fails
        """
        import multiprocessing

        workers = []
        def worker_write_func(this_obj, this_buffer):
            """
            Function used by individual processes
            """
            while len(this_buffer) > 0:
                row = this_buffer.pop()
                this_obj.write(row, validate=True)

        # number of processes
        for i in range(10):
            p = multiprocessing.Process(target=worker_write_func,
                                        args=(self, buffer))
            workers.append(p)
            p.start()

    def readAll(self):
        """
        Read all rows from the csv file and return them

        Returns:
            list: all rows from the file
        """
        with self.open_read() as csv_file:
            all_rows = [row for row in csv_file]
        return all_rows

    def read_rows_by_indices(self, row_indices):
        """
        Read and return row in the csv of index given by `row_idx`

        Args:
            row_idx (list): list of int row indices to return from the file
        """
        found = []
        all_rows = self.read_all()
        for idx, row in enumerate(all_rows):
            for row in row_indices:
                if row_idx == idx:
                    found.append(row)
        return found

    def print_all(self):
        """
        Print all rows in the csv
        """
        with self.open_read() as csv_file:
            for row in csv_file:
                print(row)
