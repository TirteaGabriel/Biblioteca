from flask import Blueprint, flash, render_template, request, redirect, session, url_for
from extension import db
from models import User, Book
from werkzeug.security import generate_password_hash, check_password_hash

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('app_routes.login'))
    
    user = User.query.filter_by(id=session['user_id']).first()
    if not user:
        flash('Utilizatorul nu a fost găsit.', 'error')
        return redirect(url_for('app_routes.login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()
        flash('Datele au fost actualizate cu succes!', 'success')
        return redirect(url_for('app_routes.profile'))

    return render_template('profile.html', user=user)

@app_routes.route('/')
def home():
    return render_template('login.html')

@app_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # verifică dacă userul există deja (opțional)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username-ul există deja!')
            return redirect(url_for('app_routes.signup'))
        
        # creează userul și setează parola
        user = User(username=username)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Cont creat cu succes!')
        return redirect(url_for('app_routes.login'))
    
    return render_template('signup.html')

@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('app_routes.dashboard'))
        else:
            flash('Username sau parola incorectă.', 'error')

    return render_template('login.html')

@app_routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('app_routes.login'))
    books = Book.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', books=books)

@app_routes.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        status = request.form['status']
        new_book = Book(title=title, author=author, genre=genre, status=status, user_id=session['user_id'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('app_routes.dashboard'))
    return render_template('add_book.html')

@app_routes.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('app_routes.dashboard'))

@app_routes.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('app_routes.login'))
