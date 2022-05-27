from importlib.resources import path
from select import select
from pydocstyle import check
from pycodestyle_autoformatter import cli, pydoc_formatter
from os.path import abspath
import pytest
from click.testing import CliRunner
import os
import shutil

DUMMY_FILES_FOLDER = 'tests/D400/'
DUMMY_TMP_FILES_FOLDER = 'tests/D400/tmp/'
DUMMY_MISSING_PERIOD_FILENAME = 'single_missing_period.py'


@pytest.fixture()
def create_single_missing_period():
    src = os.path.join(DUMMY_FILES_FOLDER, DUMMY_MISSING_PERIOD_FILENAME)
    dst = os.path.join(DUMMY_TMP_FILES_FOLDER, DUMMY_MISSING_PERIOD_FILENAME)
    try:
        os.mkdir(DUMMY_TMP_FILES_FOLDER)
        shutil.copyfile(src=src, dst=dst)
        yield dst
    finally:
        shutil.rmtree(DUMMY_TMP_FILES_FOLDER)


def assert_errors(filename, number_of_errors=0):
    pydoc_errors = list(check(filenames=[filename], select=['D400']))
    assert len(pydoc_errors) == number_of_errors


def test_file_missing_period(create_single_missing_period):
    filename = create_single_missing_period
    assert_errors(filename=filename, number_of_errors=1)
    pydoc_formatter.format_file_d400(filename)
    assert_errors(filename=filename, number_of_errors=0)


def test_cli(create_single_missing_period):
    runner = CliRunner()
    filename = create_single_missing_period
    assert_errors(filename=filename, number_of_errors=1)
    result = runner.invoke(cli.fix_D400, [filename])
    assert_errors(filename=filename, number_of_errors=0)
    assert result.exit_code == 0
