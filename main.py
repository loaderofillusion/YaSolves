from flask import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'
@app.route('/')
@app.route('/promotion_image')
def index():
    return render_template('promotion_image.html')

@app.route('/choice/<planet_name>')
def choice(planet_name):
    return render_template('choices.html', planet_name=planet_name)

@app.route('/astronaut_selection', methods=['POST', 'GET'])
def selection():
    form_data = {}
    if request.method == 'POST':

        form_data = {
            'name': request.form.get('name'),
            'surname': request.form.get('surname'),
            'email': request.form.get('email', ''),
            'degree': request.form.get('degree', ''),
            'motivation': request.form.get('motivation', ''),
            'sex': request.form.get('sex', 'male'),
            'directions': request.form.getlist('directions'),
            'accept': 'accept' in request.form  # Checkbox: True/False
        }

        print("Полученные данные:", form_data)

        flash('Форма отправлена! Данные сохранены.', 'success')
        return render_template('selection.html', form_data=form_data)

    return render_template('selection.html', form_data=form_data)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')