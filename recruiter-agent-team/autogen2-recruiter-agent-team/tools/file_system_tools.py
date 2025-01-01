import os

def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)

def get_file_list_from_path(path: str) -> list[str]:
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]        