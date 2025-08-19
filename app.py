from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import uuid
from analisa_dados import analisa_dados_func
import json

with open("config.json") as arq:
    config = json.load(arq)

app = Flask(__name__)
app.secret_key = config["API_KEY"]
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.before_request
def set_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.csv'):
            unique_name = f"{uuid.uuid4()}.csv"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            uploaded_file.save(filepath)
            json_dados = analisa_dados_func(filepath, session['user_id'])
            session['json_dados'] = json_dados
            return redirect(url_for('dashboard',user_id=session['user_id']))
    return render_template('upload.html')

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    if user_id == session['user_id']:
        return render_template('index.html', uber_data=session['json_dados'])
    return "404 Not Found", 404

@app.route('/dashboard/<user_id>/tipos')
def dashboard_tipos(user_id):
    if user_id == session['user_id']:
        return send_from_directory('templates/graficos', f'{session['user_id']}tipos.html')
    return "404 Not Found", 404

@app.route('/dashboard/<user_id>/embarque')
def dashboard_embarque(user_id):
    if user_id == session['user_id']:
        return send_from_directory('templates/graficos', f'{session['user_id']}embarque.html')
    return "404 Not Found", 404

@app.route('/dashboard/<user_id>/destino')
def dashboard_destino(user_id):
    if user_id == session['user_id']:
        return send_from_directory('templates/graficos', f'{session['user_id']}destino.html')
    return "404 Not Found", 404

@app.route('/dashboard/<user_id>/horarios')
def dashboard_horarios(user_id):
    if user_id == session['user_id']:
        return send_from_directory('templates/graficos', f'{session['user_id']}horarios.html')
    return "404 Not Found", 404

if __name__ == '__main__':
    app.run()