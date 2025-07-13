from flask import Flask, render_template

# This code sets up a simple Flask web application that returns "Hello, World!" when accessed at the root URL.

app = Flask(__name__)

@app.route('/')
def indexx():
    return render_template('index.html')    

if __name__ == '__main__':
    app.run(debug=True)
