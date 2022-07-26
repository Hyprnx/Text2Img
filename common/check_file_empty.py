import os

def is_file_empty(file_path):
    """
    Check if file is empty by confirming if its size is 0 bytes or the path exists
    :return True if file empty else False
    """
    return os.path.isfile(file_path) and os.path.getsize(file_path) == 0