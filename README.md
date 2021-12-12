# Cookiecutter Deep Learning Template

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
 - Cookiecutter
   - Install [Cookiecutter Python package](https://github.com/cookiecutter/cookiecutter) with pip

Python packages:

``` bash
pip install cookiecutter
```


## To start a new project, run:

```bash
cookiecutter https://github.com/Ivo-B/CC-DL-template
```

## License

MIT. See [LICENSE](https://github.com/Ivo-B/CC-DL-template/blob/master/LICENSE) for more details.

### Based on:
[cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)

[wemake-django-template](https://github.com/wemake-services/wemake-django-template)

[Deep-Learning-In-Production](https://github.com/The-AI-Summer/Deep-Learning-In-Production)
