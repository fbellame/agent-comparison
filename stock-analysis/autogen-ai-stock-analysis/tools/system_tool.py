
def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)
