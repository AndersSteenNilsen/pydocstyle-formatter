from pydocstyle.checker import check


def format_file_d400(filename):
    pydoc_errors = check(filenames=[filename], select=['D400'])
    line_numbers = [error.line for error in pydoc_errors]
    if not line_numbers:
        return 0
    with open(filename, 'r') as file_in:
        lines = file_in.readlines()
    for i in line_numbers:
        lines[i] = lines[i].replace('\n', '.\n')
    with open(filename, 'w') as file_out:
        file_out.writelines(lines)
