import nox

PY_VERSIONS = ["3.9", "3.10"]


@nox.session(python=PY_VERSIONS)
def formatcheck(session):
    session.install("black")
    session.run("black", "--check", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def typecheck(session):
    session.install("mypy")
    # session.run("pip", "install", "-r", "mypy_requirements.txt")
    # session.run("mypy", "--install-types", "--non-interactive")
    session.run("mypy", "--no-namespace-packages", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def lint(session):
    session.install("pylint")
    session.run("pylint", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def importscheck(session):
    session.install("isort")
    session.run("isort", "--check", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def test(session):
    session.install("pytest")
    session.run("pytest", "tests/")
