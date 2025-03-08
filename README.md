## `super_mario`

## Development Environment

We use [conda](https://conda.io/) as a package and environment manager.

1. Create an environment that includes `python` and `invoke`.
2. Activate the environment.
3. Install required packages with `bootstrap`.
4. Install this package in `develop` mode.
5. Install [git](https://git-scm.com/) `hooks`.
6. List available tasks.

```sh
$ conda create -n super_mario python=3.12 invoke --yes
$ conda activate super_mario
$ invoke bootstrap develop hooks
$ invoke --list
```

To delete

```sh
$ conda deactivate
$ conda env remove --name super_mario
```

## Check

We use various utilities to check coding style and to check for errors with static typing.

* [ruff](https://docs.astral.sh/ruff/) to make a first-pass at enforcing style rules.
* [mypy](http://www.mypy-lang.org/) to use static type checking to prevent errors.

```sh
$ invoke check --no-typing
```

To have some of these tools try to automatically fix errors, use `invoke format`. Output is best-effort and may not be
optimal.

## Test

We use [pytest](https://pytest.org/) as a test runner, and use [markers](https://docs.pytest.org/en/latest/mark.html) to
classify tests.

* `unit` - the test verifies a single unit and completes quickly (a lack of a marker implies this classification)
* `external` - the test requires an external resource
* `behavioral` - the test verifies behavior or integrates components
* `performance` - the test checks performance

We use [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) to produce code coverage reports. Code coverage is
checked when running only unit tests. Include a marker as an argument to run those tests alongside unit tests.

```sh
$ invoke test
$ invoke test --behavioral
```

See `invoke --help test` for more options.