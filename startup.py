from utils.file_checker import *
from csv_file_comparer.csv_files_comparer import CsvFilesComparer


def run():
    first_iteration = True
    first_filepath_message = "Enter path of the first file: "
    second_filepath_message = "Enter path of the second file: "
    same_files_error = "It is impossible to compare a file to itself!"
    file_comparison_completed_successfully = ("File comparison successfully completed! "
                                              "You can find its result in the file '{filename}'")
    required_file_extensions = [".csv"]

    while True:
        if first_iteration:
            first_iteration = False
        else:
            print("\n")

        old_file = _get_file(first_filepath_message, required_file_extensions)
        new_file = _get_file(second_filepath_message, required_file_extensions)

        if old_file == new_file:
            print(same_files_error)
            continue

        comparer = CsvFilesComparer(old_file, new_file)
        comparison_report_path = comparer.compare_csv_files()
        full_message_about_comparison_completed = (
            file_comparison_completed_successfully.format(filename = comparison_report_path))

        print(full_message_about_comparison_completed)


def _get_file(get_file_message: str, required_file_extensions: list[str]):
    filepath = ""

    while filepath == "":
        filepath = _get_filepath_with_message(get_file_message)
        file_validity_message = FileChecker.is_file_correct(filepath, required_file_extensions)

        if file_validity_message != "":
            print(file_validity_message)
            filepath = ""

    return filepath


def _get_filepath_with_message(message: str) -> str:
    print(message, end="")
    return input()
