import os
import sys
import csv
from datetime import datetime

from csv_file_comparer.csv_file_settings import CsvFileSettings
from csv_file_comparer.diff_report import DiffReport


class CsvFilesComparer:
    DEFAULT_COMPARISON_REPORT_NAME_PATTERN = "diff_report"
    OUTPUT_DIR = "output"

    def __init__(self, old_file: str, new_file: str, count_header_rows: int = 1):
        self._old_file = old_file
        self._new_file = new_file
        self._diff_report = DiffReport()
        self._count_header_rows = count_header_rows


    def compare_csv_files(self) -> str:
        # TODO: implement files comparison
        old_csv_file = open(self._old_file, "r", encoding=CsvFileSettings.encoding, newline=CsvFileSettings.new_line)
        new_csv_file = open(self._new_file, "r", encoding=CsvFileSettings.encoding, newline=CsvFileSettings.new_line)

        try:
            old_file_reader = csv.reader(old_csv_file, delimiter=CsvFileSettings.delimiter)
            new_file_reader = csv.reader(new_csv_file, delimiter=CsvFileSettings.delimiter)
            old_file_line = CsvFilesComparer._get_next_item_or_none(old_file_reader)
            new_file_line = CsvFilesComparer._get_next_item_or_none(new_file_reader)

            for i in range(self._count_header_rows):
                # probably mistake here
                self._diff_report.append_header_row(new_file_line)
                old_file_line = CsvFilesComparer._get_next_item_or_none(old_file_reader)
                new_file_line = CsvFilesComparer._get_next_item_or_none(new_file_reader)

                while (old_file_line is not None) and (new_file_line is not None):
                    old_row_title = old_file_line[0]
                    new_row_title = new_file_line[0]

                    if old_row_title == new_row_title:
                        # check if row is modified
                        modified_column_ids = []

                        for i in range(1, len(old_file_line)):
                            if (i >= len(new_row_title)) or (old_file_line[i] != new_file_line[i]):
                                modified_column_ids.append(i + 1)

                        if len(modified_column_ids) > 0:
                            self._diff_report.append_modified_row(new_file_line, modified_column_ids)

                        old_file_line = CsvFilesComparer._get_next_item_or_none(old_file_reader)
                        new_file_line = CsvFilesComparer._get_next_item_or_none(new_file_reader)
                    elif old_row_title > new_row_title:
                        # old file doesn't have row from the new one -> new line has been added to the new file
                        self._diff_report.append_added_row(new_file_line)
                        new_file_line = CsvFilesComparer._get_next_item_or_none(new_file_reader)
                    elif old_row_title < new_row_title:
                        # new file doesn't have row from the old one -> old line has been removed from the new file
                        self._diff_report.append_removed_row(old_file_line)
                        old_file_line = CsvFilesComparer._get_next_item_or_none(old_file_reader)

            if old_file_line is not None:
                while old_file_line is not None:
                    self._diff_report.append_removed_row(old_file_line)
                    old_file_line = CsvFilesComparer._get_next_item_or_none(old_file_reader)
            elif new_file_line is not None:
                while new_file_line is not None:
                    self._diff_report.append_added_row(new_file_line)
                    new_file_line = CsvFilesComparer._get_next_item_or_none(new_file_reader)
        finally:
            old_csv_file.close()
            new_csv_file.close()

        full_diff_report_path = self._create_diff_report()
        return full_diff_report_path


    @staticmethod
    def _get_next_item_or_none(item: csv.reader) -> any:
        try:
            next_item = next(item)
        except StopIteration:
            next_item = None

        return next_item

    def _create_diff_report(self) -> str:
        diff_report_name = CsvFilesComparer._get_diff_report_name()
        full_diff_report_path = CsvFilesComparer._get_full_diff_report_path(diff_report_name)
        self._diff_report.create_diff_report(full_diff_report_path)

        return full_diff_report_path


    @staticmethod
    def _get_diff_report_name() -> str:
        current_datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{CsvFilesComparer.DEFAULT_COMPARISON_REPORT_NAME_PATTERN}_{current_datetime_str}.xlsx"


    @staticmethod
    def _get_full_diff_report_path(report_name: str):
        current_project_directory = sys.path[1]
        output_dir = os.path.join(current_project_directory, CsvFilesComparer.OUTPUT_DIR)
        return os.path.join(output_dir, report_name)
