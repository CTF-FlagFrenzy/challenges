from flask import Flask, send_from_directory, render_template
from urllib.parse import quote as url_quote
import subprocess


app = Flask(__name__)

@app.route('/')
def index():
    subprocess.run(['python', 'flask_app/create_json.py'])
    return render_template('index.html')

@app.route('/security.txt')
def hidden_file():
    import os
    return send_from_directory(os.path.join(app.root_path, 'hidden'), 'security.txt')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)