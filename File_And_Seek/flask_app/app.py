from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the CTF challenge! Find the hidden file."

@app.route('/hidden/HaveFun.json')
def hidden_file(filename):
    return send_from_directory('hidden', filename)

if __name__ == '__main__':
    app.run(debug=True)