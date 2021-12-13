"""
Does some basic tests on the generated project.

Almost completely taken from (you guys rock!):
https://github.com/pydanny/cookiecutter-django/blob/master/tests
"""

import os
import re

import pytest
import tomlkit
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    file_list = []
    for dirpath, _subdirs, files in os.walk(root_dir):
        for file_path in files:
            file_list.append(os.path.join(dirpath, file_path))
    return file_list


def assert_variables_replaced(paths):
    """Method to check that all paths have correct substitutions."""
    assert paths, "No files are generated"

    for path in paths:
        if is_binary(path):
            continue

        with open(path, "r") as template_file:
            file_contents = template_file.read()

        match = RE_OBJ.search(file_contents)
        msg = "cookiecutter variable not replaced in {0} at {1}"

        # Assert that no match is found:
        assert match is None, msg.format(path, match.start())


def test_with_default_configuration(cookies, context):
    """Tests project structure with default prompt values."""
    baked_project = cookies.bake(extra_context=context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path.name == context["repo_name"]
    assert baked_project.project_path.is_dir()


def test_variables_replaced(cookies, context):
    """Ensures that all variables are replaced inside project files."""
    baked_project = cookies.bake(extra_context=context)
    paths = build_files_list(str(baked_project.project_path))

    assert_variables_replaced(paths)


def test_pyproject_toml(cookies, context):
    """Ensures that all variables are replaced inside project files."""
    baked_project = cookies.bake(extra_context=context)
    path = os.path.join(str(baked_project.project_path), "pyproject.toml")

    with open(path) as pyproject:
        poetry = tomlkit.parse(pyproject.read())["tool"]["poetry"]

    assert poetry["name"] == context["module_name"]
    assert poetry["description"] == context["description"]


@pytest.mark.parametrize(  # noqa: WPS317
    ("prompt", "entered_value"),
    [
        ("repo_name", "MyProject"),
        ("repo_name", "my project"),
        ("repo_name", "43project"),
        ("repo_name", "_test"),
        ("repo_name", "test_"),
        ("repo_name", "1_test"),
        ("repo_name", "test@"),
        ("repo_name", "0123456"),
    ],
)
def test_validators_work(prompt, entered_value, cookies, context):
    """Ensures that project can not be created with invalid name."""
    context = context.copy()
    context.update({prompt: entered_value})
    baked_project = cookies.bake(extra_context=context)

    assert isinstance(baked_project.exception, FailedHookException)
    assert baked_project.exit_code == -1
