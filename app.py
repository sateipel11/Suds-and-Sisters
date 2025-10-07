from flask import Flask, render_template, request
import time

app = Flask(__name__)

# Your machine data
machines = {
    "Left Washer": {"user": None, "end_time": None, "status": "available"},
    "Middle Washer": {"user": None, "end_time": None, "status": "available"},
    "Right Washer": {"user": None, "end_time": None, "status": "available"},
    "Left Dryer": {"user": None, "end_time": None, "status": "available"},
    "Right Dryer": {"user": None, "end_time": None, "status": "available"},
}


def store_form_data():
    data = {}
    data["name"] = request.form.get("username")
    data["requestedMachine"] = request.form.getlist("machines")
    return data

def setTime(machine):
    if "Washer" in machine:
        return 30*60
    if "Dryer" in machine:
        return 60*60
    return 0
    
def get_time_left(machine):
    end = machines[machine]["end_time"]
    if end is None:
        return 0
    return max(0, int(end - time.time()))

#def is_available(machine):
#    return machines[machine]["user"] is None or get_time_left(machine) == 0

# Function to reserve a machine
def reserveMachine(machine, user):
    if machines[machine]["user"] is None:
        duration = setTime(machine)
        machines[machine]["user"] = user
        machines[machine]["end_time"] = time.time() + duration
        machines[machine]["status"] = "in-use"
        return True
    return False



# ------------------------
# Routes — all at top level
# ------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        store_form_data()

        for machine in selected:
            if is_available(machine):
                machines[machine]["user"] = user
                machines[machine]["end_time"] = time.time() + get_duration(machine)

    # Send current machine status to the template
    return render_template("home.html", machines=machines)



# ------------------------
# Run the app
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#def main():
#    return 0
