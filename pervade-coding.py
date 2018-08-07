from app import app, db
from app.models import User, Award

# Not totally sure if this is useful in my context
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Award': Award}

if __name__ == '__main__':
    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('localhost', 8080, debug=True)