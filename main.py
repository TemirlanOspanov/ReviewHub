from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    category = request.form['category']
    title = request.form['title']
    rating = int(request.form['rating'])
    review_text = request.form['review']
    nick = request.form['nick']

    # Создание и сохранение отзыва
    new_review = Review(
        category=category,
        title=title,
        rating=rating,
        review_text=review_text,
        nick=nick
    )
    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('index'))


# Модель для отзывов
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    nick = db.Column(db.String(50), nullable=False)

# Инициализация базы данных
with app.app_context():
    db.create_all()

from sqlalchemy.sql import func

def get_popular_items():
    popular_items = (
        db.session.query(
            Review.title,
            Review.category,
            func.count(Review.id).label('count')
        )
        .group_by(Review.title, Review.category)
        .order_by(func.count(Review.id).desc())
        .limit(10)
        .all()
    )
    return popular_items

def get_popular_items(category=None):
    query = db.session.query(
        Review.title,
        Review.category,
        func.count(Review.id).label('count')
    )
    if category:
        query = query.filter_by(category=category)
    popular_items = (
        query.group_by(Review.title, Review.category)
        .order_by(func.count(Review.id).desc())
        .limit(10)
        .all()
    )
    return popular_items


@app.route('/')
def index():
    popular_items = get_popular_items()
    return render_template('index.html', popular_items=popular_items)

@app.route('/games')
def games():
    reviews = Review.query.filter_by(category='Игры').all()
    popular_items = get_popular_items()
    return render_template('games.html', reviews=reviews, popular_items=popular_items)

@app.route('/movies')
def movies():
    reviews = Review.query.filter_by(category='Фильмы').all()
    popular_items = get_popular_items()
    return render_template('movies.html', reviews=reviews, popular_items=popular_items)

@app.route('/series')
def series():
    reviews = Review.query.filter_by(category='Сериалы').all()
    popular_items = get_popular_items()
    return render_template('series.html', reviews=reviews, popular_items=popular_items)

@app.route('/anime')
def anime():
    reviews = Review.query.filter_by(category='Аниме').all()
    popular_items = get_popular_items()
    return render_template('anime.html', reviews=reviews, popular_items=popular_items)



if __name__ == "__main__":
    app.run(debug=True)
