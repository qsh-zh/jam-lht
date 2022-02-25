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
python run.py
```

### dev

```shell
pre-commit install # WARN: use your own pylintrc if enable pylint
```
