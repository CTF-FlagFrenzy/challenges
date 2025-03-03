import os
import subprocess
import threading
import time
import json
import tempfile

from flask import Flask, render_template, send_from_directory, jsonify, redirect, url_for, Response

app = Flask(__name__)

# Disable Flask's buffering for SSE
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

zip_creation_in_progress = False
zip_creation_complete = False
zip_creation_start_time = None
estimated_total_time = 900  # Standardwert

# Pfad zur Statusdatei
status_file_path = os.path.join(tempfile.gettempdir(), "zip_creation_status.json")

def create_zip_file():
    global zip_creation_in_progress, zip_creation_complete, zip_creation_start_time, estimated_total_time
    zip_creation_in_progress = True
    zip_creation_complete = False
    zip_creation_start_time = time.time()
    
    # Statusdatei erstellen
    with open(status_file_path, 'w') as f:
        json.dump({
            'start_time': zip_creation_start_time,
            'estimated_total_time': estimated_total_time,
            'progress': 0.0
        }, f)
    
    # Zip-Erstellungsprozess starten und Statusdatei übergeben
    subprocess.run(["python", "flask_app/create_zip.py", "--status-file", status_file_path])
    
    zip_creation_in_progress = False
    zip_creation_complete = True

def read_status_file():
    global estimated_total_time
    try:
        if os.path.exists(status_file_path):
            with open(status_file_path, 'r') as f:
                status = json.load(f)
                if 'estimated_total_time' in status and status['estimated_total_time'] > 0:
                    estimated_total_time = status['estimated_total_time']
                return status
    except Exception as e:
        print(f"Fehler beim Lesen der Statusdatei: {e}")
    
    return None

@app.route("/")
def index():
    global zip_creation_in_progress, zip_creation_complete
    
    zip_path = os.path.join(app.root_path, "zip", "HaveFun.zip")
    if os.path.exists(zip_path):
        zip_creation_complete = True
    
    if not zip_creation_in_progress and not zip_creation_complete:
        thread = threading.Thread(target=create_zip_file)
        thread.daemon = True
        thread.start()
    
    return render_template("index.html", zip_ready=zip_creation_complete, 
                          creating=zip_creation_in_progress)

@app.route("/check_status")
def check_status():
    global zip_creation_start_time, estimated_total_time, zip_creation_in_progress, zip_creation_complete
    
    # Disable buffering for SSE
    def generate():
        # Add global declaration inside the generator function
        global zip_creation_start_time
        
        zip_path = os.path.join(app.root_path, "zip", "HaveFun.zip")
        
        if os.path.exists(zip_path) or zip_creation_complete:
            data = {
                'ready': True,
                'progress': 1.0,
                'est_time_remaining': 0
            }
        else:
            # Status aus Datei lesen
            status = read_status_file()
            if status and 'progress' in status:
                progress = status['progress']
                if 'estimated_total_time' in status:
                    remaining = status['estimated_total_time'] * (1 - progress)
                    data = {
                        'ready': False,
                        'progress': progress,
                        'est_time_remaining': remaining
                    }
                else:
                    # Fallback zur alten Methode
                    current_time = time.time()
                    if zip_creation_start_time is None:
                        zip_creation_start_time = current_time
                        
                    elapsed_time = current_time - zip_creation_start_time
                    progress = min(0.99, elapsed_time / estimated_total_time)
                    
                    est_time_remaining = (estimated_total_time - elapsed_time) if progress > 0 else estimated_total_time
                    est_time_remaining = max(0, est_time_remaining)
                    
                    data = {
                        'ready': False,
                        'progress': progress,
                        'est_time_remaining': est_time_remaining
                    }
            else:
                # Fallback zur alten Methode
                current_time = time.time()
                if zip_creation_start_time is None:
                    zip_creation_start_time = current_time
                    
                elapsed_time = current_time - zip_creation_start_time
                progress = min(0.99, elapsed_time / estimated_total_time)
                
                est_time_remaining = (estimated_total_time - elapsed_time) if progress > 0 else estimated_total_time
                est_time_remaining = max(0, est_time_remaining)
                
                data = {
                    'ready': False,
                    'progress': progress,
                    'est_time_remaining': est_time_remaining
                }
        
        # Proper SSE format
        yield f"data: {json.dumps(data)}\n\n"
    
    return Response(generate(), mimetype="text/event-stream")

@app.route("/stream")
def stream():
    global zip_creation_start_time, estimated_total_time, zip_creation_in_progress, zip_creation_complete
    
    def generate():
        # Add global declaration inside the generator function
        global zip_creation_start_time
        
        while True:
            zip_path = os.path.join(app.root_path, "zip", "HaveFun.zip")
            
            if os.path.exists(zip_path) or zip_creation_complete:
                data = {
                    'ready': True,
                    'progress': 1.0,
                    'est_time_remaining': 0
                }
                yield f"data: {json.dumps(data)}\n\n"
                break  # End the stream
            
            # Status aus Datei lesen
            status = read_status_file()
            if status and 'progress' in status:
                progress = status['progress']
                if 'estimated_total_time' in status:
                    remaining = status['estimated_total_time'] * (1 - progress)
                    data = {
                        'ready': False,
                        'progress': progress,
                        'est_time_remaining': remaining
                    }
                else:
                    # Fallback zur alten Methode
                    current_time = time.time()
                    if zip_creation_start_time is None:
                        zip_creation_start_time = current_time
                        
                    elapsed_time = current_time - zip_creation_start_time
                    progress = min(0.99, elapsed_time / estimated_total_time)
                    
                    est_time_remaining = (estimated_total_time - elapsed_time) if progress > 0 else estimated_total_time
                    est_time_remaining = max(0, est_time_remaining)
                    
                    data = {
                        'ready': False,
                        'progress': progress,
                        'est_time_remaining': est_time_remaining
                    }
            else:
                # Fallback zur alten Methode
                current_time = time.time()
                if zip_creation_start_time is None:
                    zip_creation_start_time = current_time
                    
                elapsed_time = current_time - zip_creation_start_time
                progress = min(0.99, elapsed_time / estimated_total_time)
                
                est_time_remaining = (estimated_total_time - elapsed_time) if progress > 0 else estimated_total_time
                est_time_remaining = max(0, est_time_remaining)
                
                data = {
                    'ready': False,
                    'progress': progress,
                    'est_time_remaining': est_time_remaining
                }
            
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)  # Update every second
    
    return Response(generate(), mimetype="text/event-stream")

@app.route("/flag.zip")
def download_zip():
    return send_from_directory(os.path.join(app.root_path, "zip"), "HaveFun.zip")

if __name__ == "__main__":
    # Ensure we don't use caching
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)