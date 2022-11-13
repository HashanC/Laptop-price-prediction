from distutils.log import debug
from flask import Flask, render_template, request

app= Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)
