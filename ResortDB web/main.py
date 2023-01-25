from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from tables import Clients, Orders, Tarifs, Options, Services, db, app
from datetime import datetime


''' TABLES '''
@app.route('/')
@app.route('/clients')
def clients():
    clients = Clients.query
    return render_template('/tables/clients.html', title='Clients', clients=clients)

@app.route('/tarifs')
def tarifs():
    tarifs = Tarifs.query
    return render_template('/tables/tarifs.html', title='Tarifs', tarifs=tarifs)

@app.route('/orders')
def orders():
    orders = Orders.query
    return render_template('/tables/orders.html', title='Orders', orders=orders)

@app.route('/options')
def options():
    options = Options.query
    return render_template('/tables/options.html', title='Options', options=options)

@app.route('/services')
def services():
    services = Services.query
    return render_template('/tables/services.html', title='Services', services=services)
''' TABLES '''


''' CREATE '''
@app.route('/form/<table>', methods=['POST','GET'])
def form(table):
    if request.method == 'POST':
        try:
            if table == "client":
                values = Clients(name=request.form['client_name'], passport=request.form['passport'],
                                phone=request.form['phone'], address=request.form['address'])
            if table == "tarif":
                values = Tarifs(name=request.form['tarif_name'], price=request.form['tarif_price'])
            if table == "service":
                values = Services(name=request.form['service_name'], price=request.form['service_price'])
            if table == "order":
                values = Orders(client_id=request.form['order_client_id'], 
                                tarif_id=request.form['order_tarif_id'],
                                start_reserv=datetime.strptime(str(request.form['start_reserv']).replace("-", ""), "%Y%m%d").date(), 
                                ends_reserv=datetime.strptime(str(request.form['ends_reserv']).replace("-", ""), "%Y%m%d").date(), 
                                room_id=request.form['room_id'])
            if table == "option":
                values = Options(client_id=request.form['option_client_id'], service_id=request.form['option_service_id'],
                                date=datetime.strptime(str(request.form['option_date']).replace("-", ""), "%Y%m%d").date(), 
                                status=request.form['status'])
            db.session.add(values)
            db.session.commit()
            db.session.close()
            return redirect(f'/{table}s')
        except:
            db.session.rollback()
            db.session.close() 
            print("Ошибка добавления в БД")
            return redirect('/404')
    else:
        return render_template('/form.html', title=f'Create - {table}')
''' CREATE '''


''' DETAILS'''
@app.route('/info/<table>/<int:id>')
def information(table, id):
    if table == 'client':
        info = Clients.query.get(id)
        return render_template('/info.html',title=f'Client - {info.name}', info=info)
    if table == 'tarif':
        info = Tarifs.query.get(id)
        return render_template('/info.html',title=f'Tarif - {info.name}', info=info)
    if table == 'service':
        info = Services.query.get(id)
        return render_template('/info.html',title=f'Service - {info.name}', info=info)
    if table == 'order':
        info = Orders.query.get(id)        
        return render_template('/info.html',title=f'Order', info=info)
    if table == 'option':
        info = Options.query.get(id)
        return render_template('/info.html',title=f'Option', info=info)
    else:
        return redirect('/404')
''' DETAILS '''


''' DELETE '''
@app.route('/delete/<table>/<int:id>')
def delete(table, id):
    try:
        if table == 'clients':
            info = Clients.query.get(id)
        if table == 'tarifs':
            info = Tarifs.query.get(id)
        if table == 'services':
            info = Services.query.get(id)
        if table == 'orders':
            info = Orders.query.get(id)    
        if table == 'options':
            info = Options.query.get(id)
        db.session.delete(info)
        db.session.commit()
        return redirect(f'/{table}')
    except:
        db.session.rollback()
        db.session.close() 
        print("Ошибка удаления")
        return redirect('/404')
  

''' UPDATE '''
@app.route('/update/<table>/<int:id>', methods=['POST','GET'])
def update(table, id):
    if request.method == "POST":
        if table == "clients":
            client = Clients.query.get(id)
            client.name = request.form['client_name']
            client.passport = request.form['passport']
            client.phone = request.form['phone']
            client.address = request.form['address']
        if table == "tarifs":
            tarif = Tarifs.query.get(id)
            tarif.name = request.form['tarif_name']
            tarif.price = request.form['tarif_price']
        if table == "services":
            service = Services.query.get(id)
            service.name = request.form['service_name']
            service.price = request.form['service_price']
        if table == "orders":
            order = Orders.query.get(id)
            order.client_id = request.form['order_client_id']
            order.tarif_id = request.form['order_tarif_id']
            order.start_reserv = datetime.strptime(str(request.form['start_reserv']).replace("-", ""), "%Y%m%d").date()
            order.ends_reserv = datetime.strptime(str(request.form['ends_reserv']).replace("-", ""), "%Y%m%d").date()
            order.room_id = request.form['room_id']
        if table == "options":
            option = Options.query.get(id) 
            option.client_id = request.form['option_client_id']
            option.service_id = request.form['option_service_id']
            option.date = datetime.strptime(str(request.form['option_date']).replace("-", ""), "%Y%m%d").date()
            option.status = request.form['status']
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
        if table == "clients":
            info = Clients.query.get(id)
        if table == "tarifs":
            info = Tarifs.query.get(id)
        if table == "services":
            info = Services.query.get(id)
        if table == "orders":
            info = Orders.query.get(id)
        if table == "options":
            info = Options.query.get(id) 
        return render_template('/update.html', title=f'Update - {table[0:len(table)-1]} - {info.id}', info=info)
''' UPDATE '''

      
@app.route('/404')
def error():
    return render_template('/404.html')


if __name__ == '__main__':
    app.run(debug=True)
