from flask import Flask

app = Flask(__name__)

doctor_db = {
    'id': [0,1,2],
    'name': ['Doctor1', 'Doctor2', 'Doctor3'],
}

appointment_db = {
    'id': [0, 1, 2, 3, 4, 5, 6, 7],
    'doctor_id': [0, 2, 1, 2, 1, 1, 0, 0],
    'doctor_name': ['Doctor1', 'Doctor3', 'Doctor2', 'Doctor3', 'Doctor2', 'Doctor2', 'Doctor1', 'Doctor1'],
    'date': ['3/17/22', '3/17/22', '3/17/22', '3/17/22', '3/18/22', '3/17/22', '3/19/22', '3/18/22'],
    'time': ['8:00', '8:00', '8:00', '8:00', '8:30', '8:45', '16:00', '12:00'],
    'patient': ['Patient1', 'Patient2','Patient3','Patient4','Patient5','Patient6','Patient7','Patient8',],
}

@app.route("/")
def home():
    return {"Home": []}
# Members API Route
@app.route("/doctors")
def doctors():
    return doctors_db["name"]

@app.route("/appointments", methods=['GET'])
def appointments():
    body = request.get_json() # get the request body content
    
    if body is None:
        return "The request body is null", 400
    if 'doctor_name' not in body:
        return "Please specify doctor name", 400
    if 'date' not in body:
        return 'Please specify date', 400

    filtered_results = []
    selected_doctor = body['doctor_name'] 
    selected_date = body['date']

    for i in range(len(appointment_db['id'])):
        if appointment_db['doctor_name'][i] == selected_doctor and appointment_db['date'][i] == selected_date:
            filtered_results.append({
                'id': appointment_db['id'][i],
                'doctor_id':appointment_db['doctor_id'][i],
                'doctor_name':appointment_db['doctor_name'][i],
                'date': appointment_db['date'][i],
                'time': appointment_db['time'][i],
                'patient': appointment_db['patient'][i]
            })
    return filtered_results

@app.route("/appointments", methods=['DELETE'])
def delete_appointment():
    body = request.get_json()
    if 'appointment_id' not in body:
        return 'Please specify the appointment id', 400
    
    appointment_id = body['appointment_id']

    for i in range(len(appointment_db['id'])):
        if appointment_db['id'][i] == appointment_id:
            appointment_db['id'].pop(i)
            appointment_db['doctor_id'].pop(i)
            appointment_db['doctor_name'].pop(i)
            appointment_db['date'].pop(i)
            appointment_db['time'].pop(i)
            appointment_db['patient'].pop(i)
            print("Deleted Appointment: ", appointment_id)

    return appointment_db, 200

@app.route("/appointments", methods=['POST'])
def add_appointment():
    body = request.get_json()
    required_fields = ['doctor_id', 'doctor_name', 'date', 'time', 'patient']
    for field in required_fields:
        if field not in body:
            return f"Please specify the {field}", 400
        if field == 'time':
            hour, minute = body['time'].split(":")
            hour, minute = int(hour), int(minute)
            if minute % 15 != 0:
                return "Please enter a time starting at a 15-minute interval", 400
            if hour < 0 and hour > 24:
                return "Please enter a valid time", 400

    # Check that there are less than 3 appointments for a doctor at a given time
    appointment_date = body['date']
    appointment_time = body['time']
    count = 0
    for i in range(len(appointment_db['id'])):
        if appointment_db['date'][i] == appointment_date and appointment_db['time'][i] == appointment_time:
            count += 1
    if count < 3:
        appointment_db['id'].append(generate_new_appointment_id())
        appointment_db['doctor_id'].append(body['doctor_id'])
        appointment_db['doctor_name'].append(body['doctor_name'])
        appointment_db['date'].append(body['date'])
        appointment_db['time'].append(body['time'])
        appointment_db['patient'].append(body['patient'])
        return appointment_db, 200
    else:
        return f"Too many apppointments scheduled on {appointment_date}, {appointment_time}", 400


def generate_new_appointment_id():
    # Simple id generation for now, can improve later
    last_id = appointment_db['id'][-1]
    return last_id + 1


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080) 