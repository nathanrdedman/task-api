import nox

PY_VERSIONS = ["3.9", "3.10"]


@nox.session(python=PY_VERSIONS)
def formatcheck(session):
    session.install(".[develop]")
    session.run("black", "--check", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def typecheck(session):
    session.install(".[develop]")
    session.run("mypy", "--no-namespace-packages", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def lint(session):
    session.install(".[develop]")
    session.run("pylint", "src/")


@nox.session(python=PY_VERSIONS)
def importscheck(session):
    session.install(".[develop]")
    session.run("isort", "--check", "src/", "tests/")


@nox.session(python=PY_VERSIONS)
def test(session):
    session.install(".[develop]")
    session.install("-e", ".")
    session.run("pytest", "tests/")
