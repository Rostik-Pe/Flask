from market import app
from api import routes

# file  run.py executes directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
