from flask import Flask , render_template, request, redirect, url_for, Response, json
from wtforms import Form, StringField, TextAreaField, validators
from flask_assets import Bundle, Environment
import database as db

app = Flask(__name__)

css= Bundle('style.css',output='static/style.css')
assets=Environment(app)
assets.register('main_css',css)

class ArticleForm(Form):
    title = StringField('OrderId')
    body = TextAreaField('Contact Email',  [validators.Length(max=200)])

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/orders')
def orders():
	list = db.getRecords()
	return render_template('orders.html',ordereditems=list)

@app.route('/edit')
def edit():
	list = db.getRecords()
	return render_template('edit.html',ordereditems=list)

@app.route('/webhooks', methods=['GET', 'POST'])
def webhooks():
    if request.method == "GET":
        return render_template('webhook.html')
    else:
        webhook_data = json.loads(request.data)
        db.pushRecord(webhook_data)
        return Response(status=200)

@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    rec=db.getRecord(id)
    form = ArticleForm(request.form)

    form.title.data = rec['id']
    form.body.data = rec['contact_email']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        print(body)
        updates={
        	"contact_email": body
        }
        db.updateRecord(rec,updates)
        return redirect(url_for('orders'))

    return render_template('edit_order.html', form=form)

if __name__=='__main__':
	app.run(debug='True')
