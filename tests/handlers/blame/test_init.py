import argparse
import os
import tempfile

import pytest

from archeogit.handlers import blame


def _get_arguments(repository, commit):
    return argparse.Namespace(repository=repository, commit=commit)


TESTDATA = [
    ('/invalid/path/to/repository', '.* does not exist.'),
    (tempfile.gettempdir(), '.* not a valid git repository.'),
]
@pytest.mark.parametrize('repository,pattern', TESTDATA)
def test_validate_raises_argumenterror_repository(repository, pattern):
    with pytest.raises(argparse.ArgumentError, match=pattern):
        arguments = _get_arguments(repository, 'eff9507')
        blame.validate(arguments)


TESTDATA = [
    '', 'eff950', 'eff9507.', 'eff9507c1cb4b655f55d0b82cd99689892da5b64e'
]
@pytest.mark.parametrize('commit', TESTDATA)
def test_validate_raises_argumenterror_commit(commit):
    pattern = '.* is not a valid SHA-1'
    with pytest.raises(argparse.ArgumentError, match=pattern):
        arguments = _get_arguments(os.getcwd(), commit)
        blame.validate(arguments)


def test_validate():
    arguments = _get_arguments(os.getcwd(), 'eff9507')
    assert blame.validate(arguments) is None