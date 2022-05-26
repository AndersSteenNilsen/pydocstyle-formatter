from importlib.resources import path
from select import select
from pydocstyle import check
from pycodestyle_autoformatter import formatter
from os.path import abspath
import pytest
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


def test_file_missing_period(create_single_missing_period):
    filename = create_single_missing_period
    pydoc_errors = list(check(filenames = [filename],select=['D400']))
    assert pydoc_errors
    formatter.format_file_d400(filename)
    pydoc_errors = list(check(filenames = [filename],select=['D400']))
    assert not pydoc_errors


