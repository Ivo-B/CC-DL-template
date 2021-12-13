"""This module is called after project is created."""
import logging
import os
import pathlib
import shutil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("post_gen_project")

# Get the root project directory
PROJECT_DIRECTORY = pathlib.Path(os.path.abspath(os.path.curdir))
PROJECT_NAME = "{{ cookiecutter.project_name }}"
REPO_NAME = "{{ cookiecutter.repo_name }}"
MODULE_NAME = "{{ cookiecutter.module_name }}"

ALL_TEMP_FOLDERS = frozenset(("licenses",))
ALL_TEMP_FILES = frozenset((".git",))

ALL_EXAMPLE_FOLDER = frozenset((MODULE_NAME, "configs", "tests", "notebooks"))

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
    """Removes .git file, which is created because of submodule structure."""
    os.remove(PROJECT_DIRECTORY / ".git")


def get_files_in_folder(folder):
    """Yields all files recursively from a root folder."""
    for dirpath, _dirnames, filenames in os.walk(folder):
        # Remove regular files, ignore directories
        yield from tuple([os.path.join(dirpath, filename) for filename in filenames])


def remove_example_files():
    """Removes all example files, if user wants empty project."""
    if "{{ cookiecutter.add_example_code }}" == "no":  # noqa: WPS308
        for folder in ALL_EXAMPLE_FOLDER:
            for file_path in get_files_in_folder(PROJECT_DIRECTORY / folder):
                if ".gitkeep" not in file_path:
                    logger.info("Remove file: %s", file_path)
                    os.remove(file_path)


def remove_temp_folders_and_files(temp_folders, temp_files):
    """Removes all temporary folder from generate project."""
    for tmp_folder in temp_folders:
        logger.info("Remove temporary folder: %s", tmp_folder)
        shutil.rmtree(tmp_folder)
    for tmp_file in temp_files:
        logger.info("Remove temporary file: %s", tmp_file)
        os.remove(tmp_file)


def update_dotenv():
    """Creates .env based on .env.example."""
    logger.info("Creating '.env' in %s", PROJECT_DIRECTORY)
    dotenv_path = PROJECT_DIRECTORY / ".env.example"
    dotenv_path_out = PROJECT_DIRECTORY / ".env"
    with open(dotenv_path, "r") as dotenv_file:
        with open(dotenv_path_out, "w") as out_dotenv_file:
            for line in dotenv_file.readlines():
                out_line = "PROJECT_DIR={0}".format(str(PROJECT_DIRECTORY)) if "PROJECT_DIR" in line else line
                out_dotenv_file.write(out_line)


remove_temp_folders_and_files(ALL_TEMP_FOLDERS, ALL_TEMP_FILES)

remove_example_files()

update_dotenv()

print_futher_instuctions()
