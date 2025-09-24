from flask import Flask

app = Flask(__name__)

machines = {
    "Left Washer": None,
    "Middle Washer": None,
    "Right Washer ": None,
    "Left Dryer": None,
    "Right Dryer": None
}

#
#
#
#

def reserveMachine(machine, user):
    if machines[machine] is None:
        machines[machine] = user
        return True

def inputUser(time, machines, user):
    

@app.route('/')
def home():
    return '''
    <h1>Hello, Flask!</h1>
    <p>Your Flask application is running successfully!</p>
    <p><a href="/about">Visit About Page</a></p>
    '''

@app.route('/status')
def status():
    return render_template("status.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/reserve')
def reserve():
    return render_template("reserve.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)