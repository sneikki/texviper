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
