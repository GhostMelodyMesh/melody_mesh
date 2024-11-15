import re


def get_extension(file_path: str) -> str:
    extension = re.search(r'\.(\w+)$', file_path).group(1)
    return extension
