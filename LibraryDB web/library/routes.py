from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from library import app, db
from library.models import User, Books, Readers, Orders


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            
            next_page = request.args.get('next')
            print(next_page)
            if next_page == None:
                return redirect(url_for("books"))
            else:
                return redirect(next_page)
        else: 
            flash('wrong login or password')
    else:
        flash('please fill login and password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')

    if request.method == 'POST':
        if not (login or password):
            flash('login or password')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')

    return render_template('/register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('books'))
    
@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response


''' TABLES '''
@app.route('/')
@app.route('/books')
def books():
    books = Books.query
    if current_user.is_authenticated:
        books = Books.query
        return render_template('/tables/books.html', title='Books', books=books)
    else:
        return render_template('guest.html', title='Books', books=books)
    
@app.route('/readers')
@login_required
def readers():
    readers = Readers.query
    return render_template('/tables/readers.html', title='Readers', readers=readers)

@app.route('/orders')
@login_required
def orders():
    orders = Orders.query
    return render_template('/tables/orders.html', title='Orders', orders=orders)
''' TABLES '''

''' FORMS '''
@app.route('/form/<table>', methods=['POST','GET'])
@login_required
def form(table):
    if request.method == 'POST':
        # try:
            if table == "book":
                values = Books(name=request.form['name'], category=request.form['category'],
                    author=request.form['author'], year=request.form['year'])
            if table == "reader":
                values = Readers(name=request.form['name'], phone=request.form['phone'], card=request.form['card'])

            if table == "order":
                date1 = datetime.strptime(str(request.form['date1']).replace("-", ""), "%Y%m%d").date()
                date2 = datetime.strptime(str(request.form['date2']).replace("-", ""), "%Y%m%d").date()
                values = Orders(first_date=date1, second_date=date2, book_id=request.form['idbook'], reader_id=request.form['idreader'])

            
            db.session.add(values)
            db.session.commit()
            db.session.close()
            return redirect(f'/{table}s')
        # except:
        #     db.session.rollback()
        #     db.session.close() 
        #     print("Ошибка добавления в БД")
        #     return redirect('/404')
    else:
        return render_template('/form.html', title=f'{table}')
''' FORMS '''

''' DETAILS'''
@app.route('/info/<table>/<int:id>')
@login_required
def information(table, id):
    if table == 'book':
        info = Books.query.get(id)
        return render_template('/info.html',title=f'Book - {info.name}', info=info)
    if table == 'reader':
        info = Readers.query.get(id)
        return render_template('/info.html',title=f'Reader - {info.name}', info=info)
    if table == 'order':
        info = Orders.query.get(id)
        return render_template('/info.html',title=f'Order - {info.id}', info=info)
    else:
        return redirect('/404')
''' DETAILS '''

@app.route('/delete/<table>/<int:id>')
@login_required
def delete(table, id):
    # try:
        if table == 'books':
            info = Books.query.get(id)
        if table == 'readers':
            info = Readers.query.get(id)
        if table == 'orders':
            info = Orders.query.get(id)
        db.session.delete(info)
        db.session.commit()
        return redirect(f'/{table}')
    # except:
    #     db.session.rollback()
    #     db.session.close() 
    #     print("Ошибка удаления")
    #     return redirect('/404')


@app.route('/update/<table>/<int:id>', methods=['POST','GET'])
@login_required
def update(table, id):
    if request.method == "POST":
        if table == "books":
            book = Books.query.get(id)
            book.name = request.form['name']
            book.category = request.form['category']
            book.author = request.form['author']
            book.year = request.form['year']
        if table == "readers":
            reader = Readers.query.get(id)
            reader.name = request.form['name']
            reader.phone = request.form['phone']
            reader.card = request.form['card']
        if table == "orders":
            order = Orders.query.get(id)
            order.first_date = datetime.strptime(str(request.form['date1']).replace("-", ""), "%Y%m%d").date()
            order.second_date = datetime.strptime(str(request.form['date2']).replace("-", ""), "%Y%m%d").date()
            order.book_id = request.form['idbook']
            order.reader_id = request.form['idreader']
        try:
            db.session.commit()
            db.session.close()
            return redirect(f'/{table}')
        except:
            db.session.rollback()
            db.session.close() 
            print("Ошибка обновления")
            return redirect('/404')
    else:
        if table == "books":
            info = Books.query.get(id)
        if table == "readers":
            info = Readers.query.get(id)
        if table == "orders":
            info = Orders.query.get(id)

        return render_template('/update.html', title=f'Update - {table[0:len(table)-1]} - {info.id}', info=info)


@app.route('/404')
def error():
    return render_template('/404.html')
