# A bit of background

Let's say we want to create a simple database to hold arithmetic operations (add, subtract, multiply, divide) between integers. It should be easy to write new operations and read existing ones. For simplicity's sake, we will use a csv (comma-separated values) file as our database. In the `arithmetic` directory there are a handful of Python files to implement this:

- `database.py`: defines the `ArithmeticDatabase` class. This controls initialization, reading, and writing to the csv file.
- `commands.py`: contains the "work" we want to do with our database.
- `__main__.py`: sets up the command line interface.

Additionally, `example.csv` is what a csv written by this program might look like.

Code has already been committed for the desired commands. We also have a basic command and command-line interface. Now your colleague is submitting a pull request (PR) to actually create the `ArithmeticDatabase` class. Coding style is subjective, but assume that the pre-existing code (i.e. before the pull request) is styled satisfactorily. We are following [this guide](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for docstrings. As written, this code should be run using **Python 3**.

Your job is to review the code and do the following:

- find bugs that will break the code
- point out stylistic issues
- identify inefficiencies and higher level design flaws, and...
- suggest possible different approaches

If there is time, we may ask how you would further improve the code with additional features and overall architecture.

This code leverages several builtin Python libraries, a few of which are linked below:

[csv](https://docs.python.org/3/library/csv.html)

[contextlib](https://docs.python.org/3/library/contextlib.html)

[argparse](https://docs.python.org/3/library/argparse.html)
