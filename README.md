# Creating a virtual environment

If there is a python2 installation, the commands might be different.
1. python -m venv venv
2. venv\Scripts\pip install -r requirements.txt
3. venv\Scripts\python src\game_launcher\game_launcher.py

# Which python

It is important that python3 is used. I tested it with 3.7.
No guarantee that it works with lower versions.

# Interpreter options in an IDE

- Path to start script: Studienarbeit/src/game_launcher/game_launcher.py
- Working directory: Studienarbeit (Everything is based on relative paths to Studienarbeit)
- python path: Studienarbeit/venv/Scripts/python.exe
