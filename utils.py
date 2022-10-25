def file_line_count(file_name: str):
    with open(file_name, 'r') as file:
        return sum(1 for _ in file)
