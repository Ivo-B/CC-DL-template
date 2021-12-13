import pytest

default_args: dict = {
    "project_name": "My test project",
    "repo_name": "my-test-repo",
    "module_name": "mtr",
    "author_name": "Ivo Baltruschat",
    "author_mail": "im.baltruschat@icloud.com",
    "description": "A nice test project.",
    "dl_framework": "Tensorflow",
    "add_example_code": "yes",
    "license": "MIT",
}


@pytest.fixture()
def context(tmpdir) -> dict:
    """Creates default prompt values."""
    return default_args
