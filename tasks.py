from invoke import task

@task
def start(ctx):
    ctx.run('python3 src/index.py')

@task
def test(ctx):
    ctx.run('pytest src')

@task
def lint(ctx):
    ctx.run('pylint src')

@task
def reformat(ctx):
    ctx.run('autopep8 --in-place --recursive src')

@task
def coverage(ctx):
    ctx.run('coverage run --branch -m pytest src')

@task
def coverage_report(ctx):
    ctx.run('coverage html')

@task
def clean(ctx):
    ctx.run("rm -rf htmlcov .coverage")
