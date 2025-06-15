import os
import sys
import subprocess
import webbrowser
import time
from threading import Thread

def run_backend():
    """Run the Flask backend server"""
    print("Starting backend server...")
    try:
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Backend'))
        subprocess.run([sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"], check=True)
    except Exception as e:
        print(f"Error starting backend: {e}")

def open_frontend():
    """Open the frontend in the default web browser"""
    time.sleep(2)  # Give the backend a moment to start
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Front End', 'index.html')
    frontend_url = f"file:///{frontend_path.replace(os.sep, '/')}"
    print(f"Opening frontend at: {frontend_url}")
    webbrowser.open(frontend_url)

if __name__ == "__main__":
    # Start the backend in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Open the frontend
    open_frontend()
    
    print("\nTermSheet AI is now running!")
    print("- Backend API is available at: http://localhost:5000")
    print("- Frontend should open automatically in your browser")
    print("\nPress Ctrl+C to stop the application")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down TermSheet AI...")
