def file_line_count(file_name: str):
    with open(file_name, 'r') as file:
        return sum(1 for _ in file)


def remove_file_extension(file_name: str):
    return ".".join(file_name.split(".")[0:-1])
