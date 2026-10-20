import pytest

from tools import PathNotAllowed, list_files, make_read_file, read_file, safe_path


@pytest.mark.parametrize("bad", ["../README.md", "../../etc/passwd", "app/../../common.py", "/etc/passwd"])
def test_path_traversal_is_rejected(bad):
    with pytest.raises(PathNotAllowed):
        safe_path(bad)
    assert read_file(bad).startswith("Error:")
    assert list_files(bad).startswith("Error:")


def test_read_file_returns_numbered_lines():
    assert read_file("app/payments.py").splitlines()[0].startswith("1: ")


def test_list_files_shows_fixtures():
    listing = list_files()
    assert "app/payments.py" in listing and "tests/output.log" in listing


def test_narrow_reader_only_opens_assigned_files():
    narrow = make_read_file(("app/payments.py",))
    assert narrow.__name__ == "read_file"
    assert narrow("app/payments.py").startswith("1: ")
    assert narrow("tests/output.log").startswith("Error:")
