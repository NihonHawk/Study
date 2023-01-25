from flask import Flask, render_template, url_for, request, redirect
import sqlite3
import os

app = Flask(__name__)


def database_request(sql, value):
    conn = sqlite3.connect("./data.db")
    # print(sql)
    if "DELETE" in sql or "INSERT" in sql or "UPDATE" in sql:
        try:
            conn.execute(sql)
            conn.commit()
            conn.close()
        except:
            redirect('/404')
    else:
        if value == "one":
            result = conn.execute(sql).fetchone()
            conn.close()
        if value == "many":
            result = conn.execute(sql).fetchall()
            conn.close()
        return result


# /// characters ///
@app.route('/')
@app.route('/characters')
def index():
    characters = database_request("SELECT * FROM Персонажи", "many")
    return render_template('index.html', characters=characters)


@app.route('/characters/<name>')
def character_detail(name):
    character = database_request(f"SELECT * FROM Персонажи WHERE Имя = '{name}'", "one")
    print(character)
    return render_template('character-detail.html', character=character)


@app.route('/characters/<name>/del')
def character_del(name):
    database_request(f"DELETE FROM Персонажи WHERE Имя = '{name}'", None)
    return redirect('/characters')


@app.route('/characters/<name>/update', methods=['POST', 'GET'])
def character_upd(name):
    character = database_request(f"SELECT * FROM Персонажи WHERE Имя = '{name}'", "one")
    print(character)
    if request.method == 'POST':
        character = [request.form['name'], request.form['rarity'], request.form['element'], request.form['weapon'],
                     request.form['gender'], request.form['region'], request.form['bio'], request.form['const'],
                     request.form['group'], request.form['birth']]

        database_request(f"""UPDATE Персонажи SET Имя = '{character[0]}',
                                            Редкость = '{character[1]}',
                                            Элемент = '{character[2]}',
                                            Оружие = '{character[3]}',
                                            Пол = '{character[4]}',
                                            Регион = '{character[5]}',
                                            Описание = '{character[6]}',
                                            Созвездие = '{character[7]}',
                                            Группа = '{character[8]}',
                                            Деньрождения = '{character[9]}'
                                            where Имя = '{name}'
                                            """, None)
        print(character)
        return redirect('/characters')
    else:
        return render_template('character-upd.html', character=character)


# /// weapons ///
@app.route('/weapons')
def weapons():
    weapons = database_request("SELECT * FROM Оружие", "many")
    return render_template('weapons.html', weapons=weapons)


@app.route('/weapons/<name>')
def weapons_detail(name):
    weapon = database_request(f"SELECT * FROM Оружие WHERE Название = '{name}'", "one")
    return render_template('weapon-detail.html', weapon=weapon)


@app.route('/weapons/<name>/del')
def weapon_del(name):
    database_request(f"DELETE FROM Оружие WHERE Название = '{name}'", None)
    return redirect('/weapons')


@app.route('/weapons/<name>/update', methods=['POST', 'GET'])
def weapon_upd(name):
    weapon = database_request(f"SELECT * FROM Оружие WHERE Название = '{name}'", "one")
    if request.method == 'POST':
        weapon = [request.form['name'], request.form['weapon'], request.form['rarity'], request.form['attack'],
                  request.form['param'], request.form['value'], request.form['disc']]

        database_request(f"""UPDATE Оружие SET Название = '{weapon[0]}',
                            Тип = '{weapon[1]}',
                            Редкость = '{weapon[2]}',
                            Атака = '{weapon[3]}',
                            [Доп параметр] = '{weapon[4]}',
                            Значение = '{weapon[5]}',
                            Способность = '{weapon[6]}'
                            where Название = '{name}'
                            """, None)
        print(weapon)
        return redirect('/weapons')
    else:
        return render_template('weapon-upd.html', weapon=weapon)


# /// materials
@app.route('/materials')
def materials():
    materials = database_request("SELECT * FROM Материалы", "many")
    return render_template('materials.html', materials=materials)


@app.route('/materials/<name>')
def materials_detail(name):
    material = database_request(f"SELECT * FROM Материалы WHERE Название = '{name}'", "one")
    return render_template('material-detail.html', material=material)


@app.route('/materials/<name>/del')
def material_del(name):
    database_request(f"DELETE FROM Материалы WHERE Название = '{name}'", None)
    return redirect('/materials')


@app.route('/materials/<name>/update', methods=['POST', 'GET'])
def material_upd(name):
    material = database_request(f"SELECT * FROM Материалы WHERE Название = '{name}'", "one")

    if request.method == 'POST':
        material = [request.form['name'], request.form['rarity'], request.form['type'], request.form['obtain'],
                    request.form['disc']]

        database_request(f"""UPDATE Материалы SET Название = '{material[0]}',
                                                Тип = '{material[2]}',
                                                Описание = '{material[4]}',
                                                [Способ получения] = '{material[3]}',
                                                Редкость = '{material[1]}'
                                                where Название = '{name}'
                                                """, None)
        print(material)
        return redirect('/materials')
    else:
        return render_template('material-upd.html', material=material)


# /// create ///
@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/create/character', methods=['POST', 'GET'])
def create_character():
    if request.method == 'POST':
        character = [request.form['name'], request.form['rarity'], request.form['element'], request.form['weapon'],
                     request.form['gender'], request.form['region'], request.form['bio'], request.form['const'],
                     request.form['group'], request.form['birth']]

        database_request(f"""INSERT INTO Персонажи
                            VALUES (
                            '{character[0]}', '{character[1]}', '{character[2]}', '{character[3]}',
                            '{character[4]}', '{character[5]}', '{character[6]}',
                            '{character[7]}', '{character[8]}', '{character[9]}') 
                            """, None)

        return redirect('/characters'), print(character)
    else:
        return render_template('create-character.html')


@app.route('/create/weapon', methods=['POST', 'GET'])
def create_weapon():
    if request.method == 'POST':
        weapon = [request.form['name'], request.form['weapon'], request.form['rarity'], request.form['attack'],
                  request.form['param'], request.form['value'], request.form['disc']]

        database_request(f"""INSERT INTO Оружие
                            VALUES (
                            '{weapon[0]}', '{weapon[1]}', '{weapon[2]}', '{weapon[3]}',
                            '{weapon[4]}', '{weapon[5]}', '{weapon[6]}')
                            """, None)

        return redirect('/weapons'), print(weapon)
    else:
        return render_template('create-weapon.html')


@app.route('/create/material', methods=['POST', 'GET'])
def create_material():
    if request.method == 'POST':
        material = [request.form['name'], request.form['rarity'], request.form['type'], request.form['obtain'],
                    request.form['disc']]

        database_request(f"""INSERT INTO Материалы
                        VALUES (
                        '{material[0]}', '{material[1]}', '{material[2]}', '{material[3]}', '{material[4]}') 
                        """, None)

        return redirect('/materials'), print(material)
    else:
        return render_template('create-material.html')


@app.route('/recovery', methods=['POST', 'GET'])
def recovery():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Create':
            con = sqlite3.connect('data.db')
            bck = sqlite3.connect('backup.db')
            with bck:
                con.backup(bck, pages=1, progress=None)
            bck.close()
            con.close()
            print('backup created')
            return render_template('recovery.html')
        if request.form['submit_button'] == 'Restore':
            sqlite3.connect('data.db').interrupt()
            os.remove('data.db')
            con = sqlite3.connect('backup.db')
            bck = sqlite3.connect('data.db')
            with bck:
                con.backup(bck, pages=1, progress=None)
            bck.close()
            con.close()
            print('restored')
            return render_template('recovery.html')
    else:
        return render_template('recovery.html')


if __name__ == "__main__":
    app.run(debug=True)
