class FileUtils:

    @staticmethod
    def get_file_extension(filename: str) -> str:
        split_filename = filename.split('.')
        return split_filename[len(split_filename) - 1]