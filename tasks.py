import shlex
from pathlib import Path
from platform import python_version

import invoke  # http://www.pyinvoke.org/

PROJECT = "super_mario"
PACKAGE = "super_mario"
CONDA_OUTPUT = "build/conda"
DOCS_OUTPUT = "build/docs"


def current_version(ctx):
    return ctx.run("python setup.py --version", hide=True).stdout.split("\n")[-2]


@invoke.task(help={"python": "Set the python version (default: current version)"})
def bootstrap(ctx, python=python_version()):
    """Install required conda packages."""

    def ensure_packages(*packages):
        manager = "mamba"
        clean_packages = sorted({shlex.quote(package) for package in sorted(packages)})
        ctx.run(
            f"{manager} install --quiet --yes " + " ".join(clean_packages),
            pty=False,
            echo=True,
        )

    try:
        import jinja2
        import yaml
    except ModuleNotFoundError:
        ensure_packages("jinja2", "pyyaml")
        import jinja2
        import yaml

    with open("meta.yaml") as file:
        template = jinja2.Template(file.read())

    meta_yaml = yaml.safe_load(template.render(load_setup_py_data=lambda: {}, python=python))
    develop_packages = meta_yaml["requirements"]["develop"]
    build_packages = meta_yaml["requirements"]["build"]
    run_packages = meta_yaml["requirements"]["run"]

    ensure_packages(*develop_packages, *build_packages, *run_packages)


@invoke.task(help={"all": f"Remove {PACKAGE}.egg-info directory too", "n": "Dry-run mode"})
def clean(ctx, all_=False, n=False):
    """Clean unused files."""
    args = ["-d", "-x", "-e .idea", "-e .vscode"]
    if not all_:
        args.append(f"-e {PACKAGE}.egg-info")
    args.append("-n" if n else "-f")
    ctx.run("git clean " + " ".join(args), echo=True)


@invoke.task(
    help={
        "style": "Check style with flake8, isort, and black",
        "typing": "Check typing with mypy",
        "strict": "Enable strict type checking with mypy",
    }
)
def check(ctx, style=True, typing=False, strict=False):
    """Check for style and static typing errors."""
    paths = ["setup.py", "tasks.py", PACKAGE]
    if Path("tests").is_dir():
        paths.append("tests")
    if style:
        ctx.run("ruff " + " ".join(paths), echo=True)
    if typing:
        strict_arg = "--strict " if strict else ""
        ctx.run(
            f"mypy --no-incremental --show-error-codes --cache-dir=/dev/null {strict_arg}{PACKAGE}",
            echo=True,
        )


@invoke.task(name="format", aliases=["fmt"])
def format_(ctx):
    """Format code to use standard style guidelines."""
    paths = ["setup.py", "tasks.py", PACKAGE]
    if Path("tests").is_dir():
        paths.append("tests")
    ctx.run("ruff format " + " ".join(paths), echo=True)
    ctx.run("ruff check --fix " + " ".join(paths), echo=True)


@invoke.task
def test(ctx):
    """Run test"""
    ctx.run("pytest ./tests", echo=True)


@invoke.task
def install(ctx):
    """Install the package."""
    ctx.run("python -m pip install .", echo=True)


@invoke.task
def develop(ctx):
    """Install the package in editable mode."""
    ctx.run("python -m pip install --no-use-pep517 --editable .", echo=True)


@invoke.task(aliases=["undevelop"])
def uninstall(ctx):
    """Uninstall the package."""
    ctx.run(f"python -m pip uninstall --yes {PACKAGE}", echo=True)


@invoke.task
def hooks(ctx, uninstall_=False):
    """Install (or uninstall) git hooks."""

    def install_hooks():
        invoke_path = Path(ctx.run("which invoke", hide=True).stdout[:-1])
        for src_path in Path(".hooks").iterdir():
            dst_path = Path(".git/hooks") / src_path.name
            print(f"Installing: {dst_path}")
            with open(str(src_path), "r") as f:
                src_data = f.read()
            with open(str(dst_path), "w") as f:
                f.write(src_data.format(invoke_path=invoke_path.parent))
            ctx.run(f"chmod +x {dst_path}")

    def uninstall_hooks():
        for path in Path(".git/hooks").iterdir():
            if not path.suffix:
                print(f"Uninstalling: {path}")
                path.unlink()

    if uninstall_:
        uninstall_hooks()
    else:
        install_hooks()


@invoke.task(help={"linux": "Verify Linux package", "windows": "Verify Windows package"})
def verify_conda(ctx, linux=True, windows=True):
    """Verify built conda package(s)."""
    version = current_version(ctx)

    def conda_verify(platform):
        assert platform in ("linux-64", "win-64")
        ctx.run(
            f"tar -jtvf {CONDA_OUTPUT}/{platform}/{PACKAGE}-{version}-*.tar.bz2 | sort -k 6",
            echo=True,
        )
        ctx.run(
            f"conda verify {CONDA_OUTPUT}/{platform}/{PACKAGE}-{version}-*.tar.bz2",
            echo=True,
        )

    if linux:
        conda_verify("linux-64")
    if windows:
        conda_verify("win-64")


@invoke.task(help={"n": "Maximum number of releases to show (default: 10)"})
def releases(ctx, n=10):
    """Display previous releases."""
    ctx.run("git fetch --tags", hide=True)
    ctx.run(f"git tag --sort=v:refname | grep {PACKAGE} | tail -n {n}")
