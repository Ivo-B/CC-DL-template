"""
Does some basic tests on the generated project.

Almost completely taken from (you guys rock!):
https://github.com/pydanny/cookiecutter-django/blob/master/tests
"""

import os
import re
from pathlib import Path
from subprocess import PIPE, run

import chardet
import pytest
import tomlkit
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [os.path.join(dirpath, file_path) for dirpath, _subdirs, files in os.walk(root_dir) for file_path in files]


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


# TODO: update folder list
def test_verify_folders(cookies, context):
    """
    Tests that expected folders and only expected folders exist.
    """
    baked_project = cookies.bake(extra_context=context)

    expected_dirs = [
        ".",
        ".venv",
        "data",
        "data/external",
        "data/interim",
        "data/processed",
        "data/raw",
        "docs",
        "models",
        "notebooks",
        "references",
        "reports",
        "reports/figures",
        context["module_name"],
        f"{context['module_name']}/data",
        f"{context['module_name']}/features",
        f"{context['module_name']}/models",
        f"{context['module_name']}/visualization",
    ]

    expected_dirs = [Path(d) for d in expected_dirs]

    existing_dirs = [
        d.resolve().relative_to(Path(baked_project.project_path))
        for d in Path(baked_project.project_path).glob("**")
        if d.is_dir()
    ]

    assert sorted(existing_dirs) == sorted(expected_dirs)


# TODO: update file list
def test_verify_files(cookies, context):
    """
    Test that expected files and only expected files exist.
    """
    baked_project = cookies.bake(extra_context=context)

    expected_files = [
        ".env",
        ".gitignore",
        "Makefile",
        "poetry.toml",
        "pyproject.toml",
        "README.md",
        ".venv/.gitkeep",
        "data/external/.gitkeep",
        "data/interim/.gitkeep",
        "data/processed/.gitkeep",
        "data/raw/.gitkeep",
        "docs/Makefile",
        "docs/commands.rst",
        "docs/conf.py",
        "docs/getting-started.rst",
        "docs/index.rst",
        "docs/make.bat",
        "notebooks/.gitkeep",
        "references/.gitkeep",
        "reports/.gitkeep",
        "reports/figures/.gitkeep",
        "models/.gitkeep",
        f"{context['module_name']}/__init__.py",
        f"{context['module_name']}/data/__init__.py",
        f"{context['module_name']}/data/make_dataset.py",
        f"{context['module_name']}/features/__init__.py",
        f"{context['module_name']}/features/build_features.py",
        f"{context['module_name']}/models/__init__.py",
        f"{context['module_name']}/models/train_model.py",
        f"{context['module_name']}/models/predict_model.py",
        f"{context['module_name']}/visualization/__init__.py",
        f"{context['module_name']}/visualization/visualize.py",
    ]

    # conditional files
    if not context["open_source_license"].startswith("No license"):
        expected_files.append("LICENSE")

    expected_files = [Path(f) for f in expected_files]

    existing_files = [
        f.relative_to(Path(baked_project.project_path))
        for f in Path(baked_project.project_path).glob("**/*")
        if f.is_file()
    ]

    assert sorted(existing_files) == sorted(expected_files)


# def test_makefile_commands(cookies, context):
#     """
#     Actually shell out to bash and run the make commands for:
#         - create_environment
#         - requirements
#     Ensure that these use the proper environment.
#     """
#     baked_project = cookies.bake(extra_context=context)
#     test_path = Path(__file__).parent
#
#     if context["environment_manager"] == 'poetry':
#         harness_path = test_path / "poetry_harness.sh"
#     elif context["environment_manager"] == 'none':
#         return True
#     else:
#         raise ValueError(f"Environment manager '{context['environment_manager']}' not found in test harnesses.")
#
#     result = run(["bash", str(harness_path), str(baked_project.resolve())], stderr=PIPE, stdout=PIPE)
#     result_returncode = result.returncode
#
#     encoding = chardet.detect(result.stdout)["encoding"]
#     if encoding is None:
#         encoding = "utf-8"
#
#     # normally hidden by pytest except in failure we want this displayed
#     print("\n======================= STDOUT ======================")
#     print(result.stdout)
#
#     print("\n======================= STDERR ======================")
#     print(result.stderr)
#
#     assert result_returncode == 0


@pytest.mark.parametrize(
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
