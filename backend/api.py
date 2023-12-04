from flask import Flask, request, jsonify
from flask_cors import CORS
from generator import askRecentNews

app = Flask(__name__)
CORS(app)

@app.route('/greet', methods=['POST'])
def greet():
    data = request.json
    name = data['name']
    age = data['age']
    language = data['language']
    location = data['location']
    genres = data['genres']
    newsResult = askRecentNews(name, age, language, location, genres)
    return jsonify({"message": newsResult})

if __name__ == '__main__':
    app.run(debug=True)
