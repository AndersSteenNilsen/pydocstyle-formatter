from pydocstyle.checker import check
import re

FIRST_DOCSTRING_LINE_PATTERN = r'''\w[^\n"']+'''


def dot_adder(matchobj):
    return matchobj.group(0) + '.'


def correct_docstring(docstring):
    return re.sub(
        pattern=FIRST_DOCSTRING_LINE_PATTERN, repl=dot_adder, string=docstring, count=1
    )


def format_file_d400(filename):
    pydoc_errors = check(filenames=[filename], select=['D400'])
    error_docstrings = [error.definition.docstring for error in pydoc_errors]
    if not error_docstrings:
        return 0
    with open(filename, 'r') as file_in:
        file_content = file_in.read()
    for error_docstring in error_docstrings:
        fixed_docstring = correct_docstring(error_docstring)
        file_content = file_content.replace(error_docstring, fixed_docstring)
    with open(filename, 'w') as file_out:
        file_out.write(file_content)
