from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Hello, Flask!</h1>
    <p>Your Flask application is running successfully!</p>
    <p><a href="/about">Visit About Page</a></p>
    '''

@app.route('/about')
def about():
    return '''
    <h1>About</h1>
    <p>This is a simple Flask web application.</p>
    <p><a href="/">Back to Home</a></p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)