import math
from typing import Union
import tabulate


class Row:

    def __init__(self, cells):
        self.cells = cells

    def __getitem__(self, index):
        """
        Get i-th cell of the row or return a new Row object
        """
        if isinstance(index, slice):
            return Row(self.cells[index])
        else:
            return self.cells[index]

    @staticmethod
    def cosine_distance(row1, row2):
        """
        Compute the cosine distance between two rows
        """
        return 1 - Row.cosine_similarity(row1, row2)

    @staticmethod
    def cosine_similarity(row1, row2):
        """
        Compute the cosine similarity between two rows
        """
        # Calculate the dot product of the two rows
        dot_product = sum(cell1 * cell2 for cell1, cell2 in zip(row1.cells, row2.cells))

        # Calculate the magnitude of the two rows
        magnitude1 = math.sqrt(sum(cell ** 2 for cell in row1.cells))
        magnitude2 = math.sqrt(sum(cell ** 2 for cell in row2.cells))

        if magnitude1 == 0 or magnitude2 == 0:
            return -math.inf

        # Calculate the cosine similarity
        return dot_product / (magnitude1 * magnitude2)

    def __str__(self):
        row_str = ""
        for cell in self.cells:
            row_str += cell.__str__() + " "
        return row_str

    def __len__(self):
        return len(self.cells)


class Header:

    def __init__(self, columns_names):
        """
        Set the columns names
        """
        self.columns_names = columns_names

    def __getitem__(self, index):
        """
        Get i-th column name of the header
        """
        return self.columns_names[index]

    def __str__(self):
        header_str = ""
        for column_name in self.columns_names:
            header_str += column_name.__str__() + " "
        return header_str

    def append(self, column_name):
        self.columns_names.append(column_name)
        return self

    def append_at_beginning(self, column_name):
        self.columns_names.insert(0, column_name)
        return self

    def __len__(self):
        return len(self.columns_names)


class Table:

    def __init__(self, header, rows=None):
        self.header = header
        self.rows = rows if rows is not None else []

    def __getitem__(self, index) -> Union[Row, 'Table']:
        """
        Get i-th row of the table or a sliced table
        """
        if isinstance(index, slice):
            return Table(self.header, self.rows[index])
        else:
            return self.rows[index]

    def __iadd__(self, row):
        """
        Add a row to the table
        """
        self.rows.append(row)
        return self

    def __str__(self):
        """
        Print the table
        """
        return tabulate.tabulate([row.cells for row in self.rows], headers=self.header.columns_names)
