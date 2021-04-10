from invoke import task

@task
def start(ctx):
    ctx.run('python3 src/index.py --cli')

@task
def start_cli(ctx):
    ctx.run('python3 src/index.py --cli')

@task
def test(ctx):
    pass

@task
def lint(ctx):
    ctx.run('pylint src')

@task
def coverage_report(ctx):
    ctx.run("coverage html")

@task
def clean(ctx):
    ctx.run("rm -rf htmlcov .coverage")