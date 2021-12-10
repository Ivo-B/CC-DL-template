"""
This module is called after project is created.

It does the following:
1. Removes example files if is set to no!
2. Prints further instructions

"""

import os
import pathlib

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
PROJECT_NAME = "{{ cookiecutter.project_name }}"
REPO_NAME = "{{ cookiecutter.repo_name }}"
MODULE_NAME = "{{ cookiecutter.module_name }}"

# Messages
PROJECT_SUCCESS = """
Your project '{0}' is created in './{1}'.
Now you can start working on it:

    cd {1}
    poetry install
"""


def print_futher_instuctions():
    """Shows user what to do next after project creation."""
    print(PROJECT_SUCCESS.format(PROJECT_NAME, REPO_NAME))  # noqa: WPS421


# TODO:update for the example!
def remove_example_files():
    """
    Removes all example files, if user wants empty project
    :return:
    """
    project_directory = pathlib.Path(PROJECT_DIRECTORY)
    project_path = project_directory / pathlib.Path(MODULE_NAME)
    if "{{ cookiecutter.add_example_code }}" == "no":
        os.remove(project_directory / "configs" / "config.yml")
        os.remove(project_directory / "configs" / "data_shema.yml")
        os.remove(project_directory / "configs" / "logging_config.yaml")

        os.remove(project_directory / "tests" / "test_executor" / "test_prediction_model.py")
        os.remove(project_directory / "tests" / "test_models" / "test_unet.py")

        os.remove(project_path / "data" / "make_dataset.py")
        os.remove(project_path / "dataloaders" / "dataloader.py")
        os.remove(project_path / "executor" / "predict_model.py")
        os.remove(project_path / "executor" / "train_model.py")
        os.remove(project_path / "models" / "base_model.py")
        os.remove(project_path / "models" / "unet.py")
        os.remove(project_path / "utils" / "config.py")
        os.remove(project_path / "utils" / "logger.py")
        os.remove(project_path / "visualization" / "plot_image.py")
        os.remove(project_path / "visualization" / "visualize.py")
        os.remove(project_path / "main.py")


# remove_example_files()

print_futher_instuctions()
