import os
import json
import markdown
from flask import Flask, render_template_string, request, redirect, url_for
import google.generativeai as genai

# Set your Google Gemini API Key securely
genai.configure(api_key="") #Your API key here

model = genai.GenerativeModel("gemini-2.0-flash")
app = Flask(__name__)

USERS_FILE = "users.json"

# ------------------ Data Handling ------------------

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ------------------ Gemini Functions ------------------

def generate_iq_question():
    prompt = (
        "Generate a playful IQ test question. "
        "The format should be simple, suitable for web display. "
        "Include either a logic puzzle, pattern recognition, analogy, or simple MCQ."
        "Don't display answer! Just remember answer and use it later for evaluation."
        "Don't generate similar questions in a row."
    )
    response = model.generate_content(prompt)
    return markdown.markdown(response.text)

def assess_iq_change(user_answer, question_text, current_iq):
    prompt = (
        f"You're evaluating an IQ test.\n\n"
        f"Question: {question_text}\n"
        f"Answer given: {user_answer}\n"
        f"Current IQ: {current_iq}\n\n"
        "Decide how the IQ score should change (increase/decrease/same). "
        "Return only the new IQ as a number. Do not explain."
    )
    response = model.generate_content(prompt)
    try:
        new_iq = int("".join(filter(str.isdigit, response.text)))
        return new_iq
    except:
        return current_iq

# ------------------ Routes ------------------

@app.route("/", methods=["GET", "POST"])
def home():
    users = load_users()
    current_user = request.form.get("current_user") or list(users.keys())[0] if users else None
    question = None
    return render_template_string(TEMPLATE,
                                  users=users,
                                  current_user=current_user,
                                  question=None,
                                  iq=users.get(current_user, 0) if current_user else 0)

@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form.get("new_user")
    users = load_users()
    if name and name not in users:
        users[name] = 50
        save_users(users)
    return redirect(url_for("home"))

@app.route("/generate_question", methods=["POST"])
def generate_question_route():
    users = load_users()
    current_user = request.form.get("current_user")
    question = generate_iq_question()
    return render_template_string(TEMPLATE,
                                  users=users,
                                  current_user=current_user,
                                  question=question,
                                  iq=users[current_user])

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    users = load_users()
    current_user = request.form.get("current_user")
    question = request.form.get("question")
    answer = request.form.get("answer")

    current_iq = users.get(current_user, 0)
    new_iq = assess_iq_change(answer, question, current_iq)
    users[current_user] = new_iq
    save_users(users)

    return render_template_string(TEMPLATE,
                                  users=users,
                                  current_user=current_user,
                                  question=None,
                                  iq=new_iq)

# ------------------ HTML Template ------------------

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>IQ Storm</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #d3cce3, #e9e4f0);
            margin: 0; padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #4A148C;
        }
        .profile {
            margin-bottom: 20px;
        }
        .profile select, input[type="text"] {
            padding: 8px;
            margin-right: 10px;
            font-size: 1em;
        }
        .question-box {
            background: #F3E5F5;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .iq-score {
            font-size: 1.2em;
            color: #6A1B9A;
            margin-top: 10px;
        }
        button {
            background-color: #7B1FA2;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #6A1B9A;
        }
        .answer-form {
            margin-top: 20px;
        }
        .answer-form input[type="text"] {
            width: 100%;
            padding: 8px;
            font-size: 1em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🧠 IQ Storm</h1>

    <form method="POST" action="/">
        <div class="profile">
            <label for="current_user">Current User:</label>
            <select name="current_user" onchange="this.form.submit()">
                {% for user in users %}
                    <option value="{{ user }}" {% if user == current_user %}selected{% endif %}>{{ user }}</option>
                {% endfor %}
            </select>
        </div>
    </form>

    <form method="POST" action="/add_user">
        <input type="text" name="new_user" placeholder="Add New User" required>
        <button type="submit">Add</button>
    </form>

    {% if current_user %}
        <p class="iq-score"><strong>{{ current_user }}</strong>'s Current IQ: <strong>{{ iq }}</strong></p>

        <form method="POST" action="/generate_question">
            <input type="hidden" name="current_user" value="{{ current_user }}">
            <button type="submit">🧠 Generate New Question</button>
        </form>
    {% endif %}

    {% if question %}
    <div class="question-box">
        <h2>IQ Test Question:</h2>
        <p>{{ question|safe }}</p>
        <form method="POST" action="/submit_answer" class="answer-form">
            <input type="hidden" name="current_user" value="{{ current_user }}">
            <input type="hidden" name="question" value="{{ question }}">
            <input type="text" name="answer" placeholder="Your Answer" required>
            <button type="submit">Submit Answer</button>
        </form>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)
