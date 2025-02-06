from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
     if n % i == 0:
        return False
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_digit_sum(n):
    """Calculate the sum of a number's digits."""
    return sum(int(digit) for digit in str(n))

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    return n == sum(int(digit) ** len(str(n)) for digit in str(n))

def get_fun_fact(n):
    """Fetch a fun fact from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except Exception as e:
        return "Could not fetch fun fact."
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get the number from query parameters
    number = request.args.get('number')
    if not number:
        return jsonify({"number": "missing", "error": True}), 400

    # Validate that it's an integer
    try:
        number = int(number)
    except ValueError:
        return jsonify({"number": number, "error": True}), 400

    properties = []
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if is_armstrong(number):
        properties.append("armstrong")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": get_digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
