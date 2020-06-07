from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from forms import CommentForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vines.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'really very long '

db = SQLAlchemy(app)


class Vine(db.Model):
    __tablename__ = 'VINES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    sort_id = db.Column(db.Integer, db.ForeignKey('SORTS.id'))
    sort = db.relationship('Sort')
    producer_id = db.Column(db.Integer, db.ForeignKey('PRODUCERS.id'))
    producer = db.relationship('Producer')
    bestseller = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', cascade='all,delete-orphan')


class Sort(db.Model):
    __tablename__ = 'SORTS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    vines = db.relationship('Vine')


class Producer(db.Model):
    __tablename__ = 'PRODUCERS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    vines = db.relationship('Vine')


class Comment(db.Model):
    __tablename__ = 'COMMENTS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    text = db.Column(db.String)
    vine_id = db.Column(db.Integer, db.ForeignKey('VINES.id', ondelete='CASCADE'))
    vine = db.relationship('Vine')


@app.route("/")
def start():
    return redirect(url_for('index'))


@app.route("/index")
@app.route("/index/<string:sort_type>")
def index(sort_type=None):
    vines = Vine.query.all()
    if sort_type == 'byname':
        vines.sort(key=lambda x: x.name)
    if sort_type == 'bypriceasc':
        vines.sort(key=lambda x: x.price)
    if sort_type == 'bypricedesc':
        vines.sort(key=lambda x: x.price, reverse=True)
    if sort_type == 'byproducer':
        vines.sort(key=lambda x: x.producer.name)
    return render_template('index.html', vines=vines)


@app.route("/vine/<int:id>")
def vine(id):
    vine = Vine.query.get(id)
    sorts = Sort.query.all()
    producers = Producer.query.all()
    return render_template('vine.html',
                           vine=vine, sorts=sorts, producers=producers)


@app.route("/change_vine/<int:id>", methods=['post'])
def change_vine(id):
    if request.method == 'POST':
        vine = Vine.query.get(id)
        newname = request.form.get('name')
        sort_id = int(request.form.get('sort'))
        # newsort = Sort.query.get(sort_id)
        producer_id = int(request.form.get('producer'))
        # newproducer = Producer.query.get(producer_id)
        newprice = float(request.form.get('price'))
        # print(f'{name=} {id=}')
        newbestseller = int(request.form.get('bestseller') != None)

        try:
            vine.name = newname
            # vine.sort = newsort
            vine.sort_id = sort_id
            # vine.producer = newproducer
            vine.producer_id = producer_id
            vine.price = newprice
            vine.bestseller = newbestseller
            db.session.commit()
        except:
            print('не удалось изменить запись БД', id)

    return redirect(url_for('vine', id=id))


@app.route('/filter/<int:sort_id>/<int:producer_id>')
def filter(sort_id, producer_id):
    # return f'sort {sort_id}, producer {producer_id}'
    producer, sort = None, None
    if sort_id == 0:
        vines = Vine.query.filter(Vine.producer_id == producer_id)
        producer = Producer.query.get(producer_id)
    elif producer_id == 0:
        vines = Vine.query.filter(Vine.sort_id == sort_id).all()
        sort = Sort.query.get(sort_id)
    else:
        vines = Vine.query.filter(Vine.sort_id == sort_id, Vine.producer_id == producer_id).all()
        producer = Producer.query.get(producer_id)
        sort = Sort.query.get(sort_id)
    return render_template('filter.html', vines=vines, sort=sort, producer=producer)


@app.route('/delete/<int:id>')
def delete(id):
    try:
        vine = Vine.query.get_or_404(id)
        db.session.delete(vine)
        db.session.commit()
    except:
        print('не удалось удалить вино', id)
    return redirect(url_for('index'))


@app.route('/prices')
def price():
    vines = Vine.query.all()
    prices = [v.price for v in vines]
    return render_template('prices.html', vines=vines, prices=prices)


@app.route('/change_price', methods=['post'])
def change_price():
    if request.method == 'POST':
        vine_id = int(request.form.get('vine_id'))
        if vine_id > 0:
            newprice = float(request.form.get('price'))
            try:
                vine = Vine.query.get(vine_id)
                vine.price = newprice
                db.session.commit()
            except:
                print('не смогли изменить цену вина', vine_id)
        else:
            return redirect(url_for('index'))
        return redirect(url_for('price'))


@app.route('/comment/<int:id>')
def comment(id):
    vine = Vine.query.get(id)
    form = CommentForm()
    if form.validate_on_submit():
        name = form.data['name']
        email = form.data['email']
        text = form.data['text']
        try:
            comment = Comment(vine_id=id, name=name, text=text, email=email)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('vine', id=id))
        except:
            print('не удалось добавить комментарий')
    return render_template('comment.html', vine=vine, form=form)


if __name__ == '__main__':
    app.run(debug=True, port=8889)
