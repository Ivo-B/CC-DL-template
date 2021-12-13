"""This module is called before project is created."""
import logging
import re
import sys
from pathlib import Path
from subprocess import run  # noqa: S404

from cookiecutter.config import get_user_config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pre_gen_project")

REPO_NAME = "{{ cookiecutter.repo_name }}"
REPO_REGEX = r"^[a-z][a-z0-9\_\-]+[a-z0-9]$"

MODULE_NAME = "{{ cookiecutter.module_name }}"
MODULE_REGEX = r"^[a-z][a-z0-9\_]+$"


def init_git_submodule():
    """Method for executing shell command to init git submodule."""
    tmp_dir = Path(get_user_config()["cookiecutters_dir"]).absolute() / "CC-DL-template"
    logger.info("Running: git submodule update --init")
    output = run(  # noqa: S603, S607
        ["git", "submodule", "update", "--init"],
        capture_output=True,
        cwd=tmp_dir,
    )
    if output.returncode == 0:
        logger.info(output.stdout)
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
    logger.error(ex)
    sys.exit(1)

validators = (
    validate_repo_name,
    validate_module_name,
)

for validator in validators:
    try:
        validator()
    except ValueError as ex:  # noqa: WPS440
        logger.error(ex)
        sys.exit(1)
