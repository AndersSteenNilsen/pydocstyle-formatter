from fileinput import filename
from importlib.resources import path
from select import select
from pydocstyle import check
from pydocstyle_autoformatter import cli, pydoc_formatter
from os.path import abspath
import pytest
from click.testing import CliRunner
import os
import shutil

DUMMY_FILES_FOLDER = 'tests/D400/'
DUMMY_TMP_FILES_FOLDER = 'tests/D400/tmp/'
DUMMY_MISSING_PERIOD_FILENAME = 'single_missing_period.py'


@pytest.fixture(params=['single_missing_period.py', 'multi_missing_period.py', 'multi_missing_period_2.py'],
)
def create_temp_file(request):
    filename=request.param
    src = os.path.join(DUMMY_FILES_FOLDER, filename)
    dst = os.path.join(DUMMY_TMP_FILES_FOLDER, filename)
    try:
        os.mkdir(DUMMY_TMP_FILES_FOLDER)
        shutil.copyfile(src=src, dst=dst)
        yield dst
    finally:
        shutil.rmtree(DUMMY_TMP_FILES_FOLDER)


def assert_errors(filename, number_of_errors=0):
    pydoc_errors = list(check(filenames=[filename], select=['D400']))
    assert len(pydoc_errors) == number_of_errors


def test_file(create_temp_file):
    filename=create_temp_file
    assert_errors(filename=filename, number_of_errors=1)
    pydoc_formatter.format_file_d400(filename)
    assert_errors(filename=filename, number_of_errors=0)


def test_cli(create_temp_file):
    filename=create_temp_file
    runner = CliRunner()
    assert_errors(filename=filename, number_of_errors=1)
    result = runner.invoke(cli.fix_D400, [filename])
    assert_errors(filename=filename, number_of_errors=0)
    assert result.exit_code == 0
