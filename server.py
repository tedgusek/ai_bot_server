from flask import Flask, request, jsonify
from flask_cors import CORS

#app instance
app = Flask(__name__)
CORS(app)

# Create App Route /api/home
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Hello world!"
    })

@app.route("/botresponse",methods=['POST'])
def bot_response():
    # Get the JSON Payload from REQUEST
    request_data = request.get_json()

    # extract the user message
    user_message = request_data.get('user_message')

    # Logic to get the AI response
    # For now, we'll just echo the user message for demonstration purposes
    # Replace this with your AI response logic
    bot_response = f"Echo: {user_message}"

    # Return JSON response
    return jsonify({'bot_response': bot_response})


if __name__ == "__main__":
    app.run(debug=True, port=8080)