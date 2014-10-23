from flask import Flask

app = Flask('myflask_flaskapp')

@app.route('/')
@app.route('/<path:path>')
def hello_world():
    return '<h1>Hello, world!</h1>A flask app brought to you by servi.'

if __name__ == '__main__':
    app.run()