from flask import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = 'ahha'
    return render_template('index.html', user=user)

@app.route('/odd_even')
def odd_even():
    return render_template('odd_even.html'  )
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')