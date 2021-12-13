# Cookiecutter Deep Learning Template

Never have problems again when setting up a DL software project.

## Purpose

- Simplified deployment of research software and reproducibility of results for other users
- Improve and verify code quality using external tools
- Reduction of redundant tasks at project start
- Best-practices information for the successful development of a DL project

## Features

- Supports `python3.9+`
- [`poetry`](https://github.com/python-poetry/poetry) for managing dependencies
- [`mypy`](https://mypy.readthedocs.io) for static typing
- [`pytest`](https://pytest.org/) and [`hypothesis`](https://github.com/HypothesisWorks/hypothesis) for unit tests
- [`flake8`](http://flake8.pycqa.org/en/latest/) and [`wemake-python-styleguide`](https://wemake-python-styleguide.readthedocs.io/en/latest/) for linting
- [`docker`](https://www.docker.com/) for development, testing, and production
- [`sphinx`](http://www.sphinx-doc.org/en/master/) for documentation

## Requirements to use the cookiecutter template:
 - Python 3.9+
 - Cookiecutter 1.7+

Install [Cookiecutter Python package](https://github.com/cookiecutter/cookiecutter) with pip
``` bash
pip install cookiecutter
```

## To start a new project, run:

```bash
cookiecutter https://github.com/Ivo-B/CC-DL-template
```

Cookiecutter prompts you for information regarding your plugin:
```
project_name [Unique Project Name]:
repo_name [unique-project-name]:
module_name [uniqueprojectname]:
author_name [Your name]:
author_mail [Your.name@email.com]:
description [A short description of the project.]:
Select dl_framework:
1 - Tensorflow
2 - PyTorch
Choose from 1, 2, 3 [1]:
Select add_example_code:
1 - yes
2 - no
Choose from 1, 2 [1]:
Select license:
1 - MIT
2 - BSD-3
3 - Apache-2.0
4 - GNU GPL v3.0
5 - Mozilla Public License 2.0
6 - none
Choose from 1, 2, 3, 4, 5, 6 [1]:
```

## License

MIT. See [LICENSE](https://github.com/Ivo-B/CC-DL-template/blob/master/LICENSE) for more details.

### Based on:
[cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)

[wemake-django-template](https://github.com/wemake-services/wemake-django-template)

[Deep-Learning-In-Production](https://github.com/The-AI-Summer/Deep-Learning-In-Production)
