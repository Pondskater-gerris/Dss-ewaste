from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response, json
import json
from flask_cors import CORS
from flask_session import Session
from flask import flash,get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)
app.config['SECRET_KEY'] = 'Pondskatergerris123'


# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

#Initialize sesion management 
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

# Define model for session data
class SessionData(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = {'extend_existing': True}  # Add this line
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    data = db.Column(db.Text, nullable=False)

    def __init__(self, session_id, data):
        self.session_id = session_id
        self.data = json.dumps(data)  # Serialize final_values to JSON

    def get_final_values(self):
        return json.loads(self.data)  # Deserialize final_values from JSON
    
@app.route('/')
@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/help.html')
def help():
    return render_template('help.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/glossary.html')
def glossary():
    return render_template('glossary.html')

@app.route('/start.html')
def start():
    return render_template('start.html')

@app.route('/Results.html')
def Results():
    return render_template('Results.html')

'''@app.route('/Product_modeling', methods=['GET','POST','OPTIONS'])
def product_page():
    if request.method == 'POST':
        try:
            # Get JSON data from the request
            data = request.json

            # Process the form data as needed
            # For demonstration, just print the data
            print("Received form data:")
            print(data)

            # Perform any other processing or database operations here

            # Return success response
            return jsonify({"status": "success", "message": "Form submitted successfully"})

        except Exception as e:
            # Handle any exceptions or errors
            return jsonify({"status": "error", "message": str(e)})
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({"status": "success"})
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    # Return a different response for GET requests if needed
    return jsonify({"status": "error", "message": "GET request received, expected POST"})'''



@app.route('/Product_modeling', methods=['GET', 'POST', 'OPTIONS'])
def Product_modeling_page():
    if request.method == 'POST':
        try:
            # Your existing data processing logic...
            data = request.get_json()
            

            #Default values for cost of waste treatment
            # Define the default values for waste streams
            default_waste_costs = {
                'Metals': 781.1,
                'Plastic': 781.1,
                'Cables': 635.1,
                'Control Units': 1054.85,
                'Panels': 1054.85,
                'Lithium Batteries': 1237.35,
                'Mixed Solar': 974.55,
            }


            # Access form data
            selectedProducts = data.get('selectedProducts')
            #starting_year = data.get('startingYear')
            #number_of_years = data.get('numberOfYears')
            defaultValuesToggle = data.get("defaultValuesToggle")
            wasteTreatmentToggle = data.get("wasteTreatmentToggle")
            metalsInput = data.get("metalsInput")
            plasticInput = data.get("plasticInput")
            cablesInput = data.get("cablesInput")
            controlUnitsInput = data.get("controlUnitsInput")
            panelsInput = data.get("panelsInput")
            mixedSolarInput = data.get("mixedSolarInput")
            lithiumBatteriesInput = data.get("lithiumBatteriesInput")
            #batteryPercentage = data.get("batteryPercentage")
            # Access matrix table data
            #matrix_table = data.get('matrixTable')
            # Access matrix Input Data data
            matrixInputData = data.get('matrixInputData')

            #Create dictionary for input user waste stream cost 
            input_waste_costs = {
                'Metals': metalsInput,
                'Plastic': plasticInput,
                'Cables': cablesInput,
                'Control Units': controlUnitsInput,
                'Panels': panelsInput,
                'Lithium Batteries': lithiumBatteriesInput,
                'Mixed Solar': mixedSolarInput,
            }

            # Create a dictionary to store the default values
            defaultValues = {
                'T1': {'weight': 0.001, 'lifespan': 3.3, 'shape': 7.0, 'scale': 3.5},  # Adjust with your default values
                'T2': {'weight': 0.004, 'lifespan': 3.7, 'shape': 7.0, 'scale': 4.0},  # Adjust with your default values
                'T3': {'weight': 0.005, 'lifespan': 8.5, 'shape': 8.0, 'scale': 9.0},   # Adjust with your default values
                'T4': {'weight': 0.007, 'lifespan': 8.5, 'shape': 8.0, 'scale': 9.0},  # Adjust with your default values
                'Lead Acid Battery': {'weight': 0.003, 'lifespan': 2.7, 'shape': 2.0, 'scale': 3.0},  # Adjust with your default values
                'Lithium Ion Battery': {'weight': 0.001, 'lifespan': 3.7, 'shape': 7.0, 'scale': 4.0},  # Adjust with your default values
                'Mini-Grids': {'weight': 8.0, 'lifespan': 25.7, 'shape': 10.0, 'scale': 27.0},  # Adjust with your default values
                'Lead Acid Battery -Minigrid': {'weight': 0.150, 'lifespan': 2.7, 'shape': 2.0, 'scale': 3.0},  # Adjust with your default values
                'Lithium Ion Battery -Minigrid': {'weight': 0.050, 'lifespan': 8.9, 'shape': 8.0, 'scale': 9.5},  # Adjust with your default values

            }

            # Set conditions for defining final values
            # Create a dictionary to store the final values
            final_values = {}

            # Iterate through selected products
            for product in selectedProducts:
                # Check the status of defaultValuesToggle
                if defaultValuesToggle == 'on':
                    # Use default values for weight, lifespan, shape, and scale
                    final_values[product] = defaultValues[product]
                else:
                    # Use user-entered values for weight and lifespan, default values for shape and scale
                    final_values[product] = {
                        'weight': next(item['weight'] for item in matrixInputData if item['product'] == product),
                        'lifespan': next(item['lifespan'] for item in matrixInputData if item['product'] == product),
                        'shape': defaultValues[product]['shape'],
                        'scale': defaultValues[product]['scale'],
                    }

            # Check the status of wasteTreatmentToggle
            if wasteTreatmentToggle == 'on':
                waste_costs = default_waste_costs
            else:
                waste_costs = input_waste_costs

            print(f"finalvalues: {final_values}")


            # Store final_values in the session
            session['final_values'] = final_values

            # Serialize final_values before storing in the database
            final_values_json = json.dumps(final_values)

            # Save session data to the database

            final_values_json = json.dumps(final_values)  # Serialize final_values to JSON

            db.session.add(SessionData(session_id=session.sid, data=final_values_json))
            db.session.commit()

            print(f"Final values: {final_values}")
            # Redirect to the show_data_page
            #return redirect(url_for('matrix_page'))
            #return print(type(final_values))
            

        except Exception as e:
            # Handle any exceptions or errors
            return jsonify({"status": "error", "message": str(e)})

    # Handle OPTIONS request...
    if request.method == 'OPTIONS':
        response = jsonify({"status": "success"})
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    return jsonify({"status": "error", "message": "GET request received, expected POST"})


    # Render the template with the final_values
    #return render_template('matrix.html')


'''@app.route('/matrix_page', methods=['POST','GET', 'OPTIONS'])
def matrix_page():

    if request.method == 'POST':
        # Retrieve session data from the database
        session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        session_data = SessionData.query.filter_by(session_id=session_id).first()

        print(f"finalvalues under POST: {session_data}")


        # Deserialize session data if it exists
        final_values = {}
        if session_data:
            final_values = session_data.get_final_values()

        print(f"finalvalues under POST: {final_values}")

        # Render the show_data_page template with the final_values
        return render_template('matrix.html', final_values=final_values)
    
    if request.method == 'GET':
        # Retrieve session data from the database
        session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        session_data = SessionData.query.filter_by(session_id=session_id).first()

        print(f"finalvalues under GET: {session_data}")


        # Deserialize session data if it exists
        final_values = {}
        if session_data:
            final_values = session_data.get_final_values()

        print(f"finalvalues under GET: {final_values}")
        return render_template('matrix.html', final_values=final_values)

    
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")

        # Retrieve session data from the database
        session_id = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        session_data = SessionData.query.filter_by(session_id=session_id).first()

        print(f"finalvalues under OPTIONS: {session_data}")


        # Deserialize session data if it exists
        final_values = {}
        if session_data:
            final_values = session_data.get_final_values()

        print(f"finalvalues under OPTIONS: {final_values}")
        return response

    return jsonify({"status": "error", "message": "GET request received, expected POST"})'''



if __name__ == '__main__':
    app.run(debug=True)
