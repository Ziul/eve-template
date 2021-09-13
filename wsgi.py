"""
Gunicorn app to run API without debug flag as default
"""

from main import app as application

if __name__ == "__main__":
    application.run()
