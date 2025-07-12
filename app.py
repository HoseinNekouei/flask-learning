from flask import Flask

# This code sets up a simple Flask web application that returns "Hello, World!" when accessed at the root URL.

app = Flask(__name__)

@app.route('/')
def indexx():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
