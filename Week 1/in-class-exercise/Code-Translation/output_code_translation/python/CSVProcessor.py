import os

class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name):
        """
        Returns a tuple (title, data)
        title: list of column headers
        data: list of rows, each a list of strings
        """
        title = []
        data = []
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                # Read header line
                line = f.readline()
                if line:
                    title = line.rstrip('\n').split(',')
                # Read remaining lines
                for line in f:
                    row = line.rstrip('\n').split(',')
                    data.append(row)
        except (IOError, OSError):
            # File could not be opened; return empty structures
            pass
        return title, data

    def write_csv(self, data, file_name):
        """
        Writes `data` (list of rows) to `file_name`.
        Returns 1 on success, 0 on failure.
        """
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                for row in data:
                    f.write(','.join(row))
                    f.write('\n')
            return 1
        except (IOError, OSError):
            return 0

    def process_csv_data(self, N, save_file_name):
        """
        Extracts column N from the CSV, converts its entries to uppercase,
        and writes a new CSV containing the original header and the processed column.
        Returns 1 on successful write, 0 otherwise.
        """
        title, data = self.read_csv(save_file_name)
        if not data or N >= len(data[0]):
            return 0

        column_data = []
        for row in data:
            if N < len(row):
                column_data.append(row[N].upper())

        new_data = [title, column_data]

        base, ext = os.path.splitext(save_file_name)
        new_file_name = f"{base}_process.csv"
        return self.write_csv(new_data, new_file_name)
