import flask

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def home():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run()