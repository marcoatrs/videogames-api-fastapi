from fastapi import FastAPI

app = FastAPI(
    title='App con FastAPI',
    version='0.0.1'
)


@app.get('/', tags=['home'])
def main():
    return 'Hello World'
