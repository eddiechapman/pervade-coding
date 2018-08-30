from app import app, db
from app.models import User, Award


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Award': Award}

if __name__ == '__main__':
    app.run('localhost', 8080, debug=False)