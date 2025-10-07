from flask import Flask, render_template, request
import time

app = Flask(__name__)

# Machine data
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

#TIMER FUNCTIONS
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
#function to display minutes left for the front-end 
def get_time_left_minutes(machine):
    seconds_left = get_time_left(machine)
    if seconds_left >= 60:
        return f"{seconds_left // 60} min"
    elif seconds_left > 0:
        return f"{seconds_left} sec"
    else:
        return "0 sec"

#RESERVING FUNCTIONS
#check if machine can be reserved (if available)
def is_available(machine):
    return machines[machine]["status"] == "available"


# Function to reserve a machine
def reserveMachine(machine, user):
    if machines[machine]["user"] is None:
        duration = setTime(machine)
        machines[machine]["user"] = user
        machines[machine]["end_time"] = time.time() + duration
        machines[machine]["status"] = "in-use"
        return True
    return False
    
def update_machine_times():
    for machine in machines:
        if get_time_left(machine) <= 0 and machines[machine]["status"] == "in-use":
            machines[machine]["status"] = "finished"

def clear_machine(machine):
    machines[machine]["user"] = None
    machines[machine]["end_time"] = None
    machines[machine]["status"] = "available"




# ------------------------
# Routes — all at top level
# ------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    # Update machines automatically if timers done
    update_machine_times()

    if request.method == "POST":
        data = store_form_data()
        user = data["name"]
        selected = data["requestedMachine"]

        #which form was submitted
        form_type = request.form.get("form_type")

        if form_type == "reserve":
            if user.strip() != "":  # only reserve if user entered a name
                for machine in selected:
                    if is_available(machine):
                        reserveMachine(machine, user)

        elif form_type == "remove":
            # Clear selected
            for machine in selected:
                clear_machine(machine)

    # Calculate time left in minutes
    time_left_minutes = {m: get_time_left_minutes(m) for m in machines}

    # Render template
    return render_template("home.html", machines=machines, time_left=time_left_minutes)




# ------------------------
# Run the app
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#def main():
#    return 0
