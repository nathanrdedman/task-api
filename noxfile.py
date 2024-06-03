import nox

PY_VERSIONS = ["3.9", "3.10"]


@nox.session(python=PY_VERSIONS)
def test(session):
    session.install("pytest")
    session.run("pytest", "test/")


@nox.session(python=PY_VERSIONS)
def formatcheck(session):
    session.install("black")
    session.run("black", "--check","src/", "test/")


@nox.session(python=PY_VERSIONS)
def typecheck(session):
    session.install("mypy", "pytest")
    session.run("mypy", "src/", "test/")


@nox.session(python=PY_VERSIONS)
def lint(session):
    session.install("pylint")
    session.run("pylint", "src/", "test/")
