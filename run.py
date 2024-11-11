# Di awal run.py
import sys
import os
import platform

if platform.system() != 'Windows':
    import fcntl
    
print("Python path:", sys.path)
print("Current directory:", os.getcwd())
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()