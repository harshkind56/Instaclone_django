from instaclone.celery import app

@app.task(name = 'sum')
def add(x, y):
    return x+y