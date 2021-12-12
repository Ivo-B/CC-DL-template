"""
This module is called after project is created.
"""
import logging
import os
import pathlib
import shutil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("post_gen_project")

# Get the root project directory
PROJECT_DIRECTORY = os.path.abspath(os.path.curdir)
PROJECT_NAME = "{{ cookiecutter.project_name }}"
REPO_NAME = "{{ cookiecutter.repo_name }}"
MODULE_NAME = "{{ cookiecutter.module_name }}"

ALL_TEMP_FOLDERS = []
ALL_TEMP_FILES = [".git"]

ALL_EXAMPLE_FOLDER = ["configs", MODULE_NAME, "tests", "notebooks"]

# Messages
PROJECT_SUCCESS = """
Your project '{0}' is created in '{1}'.
First, read the documentation to familiarize yourself with the template.
Secondly, now you can start working on it:
    cd {1}
    make environment
"""


def print_futher_instuctions():
    """Shows user what to do next after project creation."""
    print(PROJECT_SUCCESS.format(PROJECT_NAME, REPO_NAME))  # noqa: WPS421


def remove_git_file():
    """Removes .git file, which is created because of submodule structure"""
    project_path = pathlib.Path(PROJECT_DIRECTORY)
    os.remove(project_path / ".git")


def remove_example_files():
    """Removes all example files, if user wants empty project"""
    if "{{ cookiecutter.add_example_code }}" == "no":
        project_directory = pathlib.Path(PROJECT_DIRECTORY)
        for folder in ALL_EXAMPLE_FOLDER:
            for dirpath, dirnames, filenames in os.walk(project_directory / folder):
                # Remove regular files, ignore directories
                for filename in filenames:
                    logger.info("Remove file: %s", os.path.join(dirpath, filename))
                    os.remove(os.path.join(dirpath, filename))


def remove_temp_folders_and_files(temp_folders, temp_files):
    for folder in temp_folders:
        logger.info("Remove temporary folder: %s", folder)
        shutil.rmtree(folder)
    for file in temp_files:
        logger.info("Remove temporary file: %s", file)
        os.remove(file)


remove_temp_folders_and_files(ALL_TEMP_FOLDERS, ALL_TEMP_FILES)

remove_example_files()

print_futher_instuctions()
