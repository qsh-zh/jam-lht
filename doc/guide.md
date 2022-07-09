# quickstart

### search keyword `# TODO: setme` and overwrite
### install dependency


*[poetry](https://python-poetry.org/)* (**recommended**)
```shell
#poetry
poetry install --no-dev # minimal package
poetry install # whole package
```

*pip* (not recommended)
```shell
pip install -U pip setuptools
pip install -e .
```

### run

```shell
# see more on README.md
python main.py
```

### dev

```shell
pre-commit install # WARN: use your own pylintrc if enable pylint
# install torch
poe cuda13
```

## dev dep

```shell
poetry add jammy==0.0.9 --dev
```

## to pip

```shell
poetry export -f requirements.txt > requirements.txt
python -m pip install -r requirements.txt
poetry install
```

## issue

- [module 'distutils' has no attribute 'version'](https://github.com/pytorch/pytorch/issues/69894) `poetry add setuptools@latest`
