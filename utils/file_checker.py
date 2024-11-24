import os


class FileChecker:
    @staticmethod
    def is_file_correct(filepath: str, required_extensions: list[str] = None) -> str:
        if filepath == "":
            return "Filepath is empty!"

        if not FileChecker._is_filepath_correct(filepath):
            return f"Cannot access to the file '{filepath}'!"

        if not FileChecker._has_file_correct_extension(filepath, required_extensions):
            return f"File {filepath} has invalid extension!"

        return ""


    @staticmethod
    def _is_filepath_correct(filepath: str) -> bool:
        return os.path.isfile(filepath)


    @staticmethod
    def _has_file_correct_extension(filepath: str, required_extensions: list[str] = None) -> bool:
        if (required_extensions is None) or (len(required_extensions) == 0):
            return True

        for extension in required_extensions:
            if filepath.endswith(extension):
                return True

        return False
