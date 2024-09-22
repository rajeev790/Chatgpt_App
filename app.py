from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import openai
from search_index import search_documents

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# OpenAI API key
openai.api_key = 'your_openai_api_key'

# PostgreSQL Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chatgpt_user:your_password@localhost/chatgpt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_input = request.json.get('message')
    response = openai.Completion.create(
        model="gpt-4",  # Use the latest model
        prompt=user_input,
        max_tokens=150
    )
    return jsonify(response['choices'][0]['text'].strip())

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    results = search_documents(query)
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
