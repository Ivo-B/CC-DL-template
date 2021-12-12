"""
This module is called before project is created.

It does the following:
1. Checks `repo_name` for correct naming
2. Checks `module_name` for correct naming

"""

import re
import sys
import subprocess

REPO_NAME = "{{ cookiecutter.repo_name }}"
REPO_REGEX = r"^[a-z][a-z0-9\_\-]+[a-z0-9]$"

MODULE_NAME = "{{ cookiecutter.module_name }}"
MODULE_REGEX = r"^[a-z][a-z\_]+[a-z]$"


def init_git_submodule():
    """Method for executing shell command to init git submodule."""
    print("Running: git submodule update --init")  # noqa: WPS421
    output = subprocess.run(["git", "submodule", "update", "--init"], capture_output=True)
    if output.returncode == 0:
        print(output.stdout)
    else:
        raise ValueError("ERROR: {0} .".format(output.stderr))


def validate_repo_name():
    """This validator is used to ensure that `repo_name` is valid.
    Valid example: `school_project3`.
    Valid example: `school-project3`.
    """
    if not re.match(REPO_REGEX, REPO_NAME):
        # Validates project's repo name:
        message = [
            "ERROR: The project slug {0} is not a valid name.",
            "Start with a lowercase letter.",
            "Followed by any lowercase letters, numbers, underscores (_), or dashes (-).",
            "End with a lowercase letter or number.",
        ]
        raise ValueError(" ".join(message).format(REPO_NAME))


def validate_module_name():
    """This validator is used to ensure that `module_name` is valid.
    Valid example: `school_project`.
    """
    if not re.match(MODULE_REGEX, MODULE_NAME):
        # Validates project's module name:
        message = [
            "ERROR: The project slug {0} is not a valid name.",
            "Start with a lowercase letter.",
            "Followed by any lowercase letters or underscores (_).",
            "End with a lowercase letter.",
        ]
        raise ValueError(" ".join(message).format(MODULE_NAME))


try:
    init_git_submodule()
except ValueError as ex:
    print(ex)  # noqa: WPS421
    sys.exit(1)

validators = (
    validate_repo_name,
    validate_module_name,
)

for validator in validators:
    try:
        validator()
    except ValueError as ex:
        print(ex)  # noqa: WPS421
        sys.exit(1)