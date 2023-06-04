"""Description"""
# import folium
from flask import redirect, render_template, request, url_for

# from app.maps import map
from bod.mongodb_connection import bod, bod_users

from . import app
from .forms import (FilterForm, LengthSelector, LoginForm, RegisterForm,
                    SearchForm)
from .models import Addrobj, Addrobj_list, House, House_list


@app.route('/')
@app.route('/home')
def home():
    title = 'BOD | Main'
    heading = 'Main page'
    content = 'Привет! Хочешь зарегистрироваться?'

    return render_template('index.html',
                           title=title,
                           heading=heading,
                           content=content)


@app.route('/api/data')
def get_data():
    return app.send_static_file('data.json')


@app.route('/about')
def about():
    title = 'BOD | About'
    heading = 'About'
    content = 'Example app page for Flask.'

    return render_template('about.html',
                           title=title,
                           heading=heading,
                           content=content)


@app.route('/tables')
def tables():
    title = 'BOD | Tables'
    colls_list = bod.list_collections

    content = []
    for coll in colls_list:
        link = '/tables/' + coll + '/1'
        content.append({'name': coll, 'link': link})

    return render_template('tables.html',
                           title=title,
                           colls_list=content)


@app.route('/tables/<collection_name>/<page_num>', methods=['GET', 'POST'])
def tables_example(collection_name, page_num):
    coll = bod.get_collection(collection_name)
    coll_size = coll.mongo.count_documents({})
    table_name = f'{collection_name} | Page {str(page_num)} | {str(coll_size)} documents'
    data = list(coll.mongo.find({}).limit(20).skip(20*(int(page_num)-1)))
    headings = list(data[0].keys())
    for_paginator = [int(page_num)-1, int(page_num), int(page_num)+1]
    link = f'/tables/{collection_name}'
    searchform = SearchForm()
    filterform = FilterForm()

    mes = ''
    if request.method == 'POST':
        mes = searchform.search.data

    return render_template('tables_example.html',
                           title=f'BOD | {collection_name}',
                           table_name=table_name,
                           searchform=searchform,
                           filterform=filterform,
                           for_paginator=for_paginator,
                           link=link,
                           data=data,
                           headings=headings,
                           mes=mes)


@app.route('/addrobjs/<page>', methods=['GET', 'POST'])
def addrobjs(page):
    title = 'BOD | Address Objects'
    heading = 'Address Objects'
    # TO DO Выбирать length из селектора (12, 24, 48, 96)
    length_selector = LengthSelector()
    if request.method == 'POST':
        length = LengthSelector().selector.data
    else:
        length = 0
    default_length = 12
    if length == 0:
        length = default_length
    length = 12
    for_paginator = [int(page)-1, int(page), int(page)+1]
    link = '/addrobjs'
    data = Addrobj_list.get_data(limit=length, skip=length*int(page)-1)
    data_keys = data.keys()
    link_to_house = []
    for s in data_keys:
        link_to_house.append('/addrobj/' + s)

    return render_template('addrobjs.html',
                           title=title,
                           heading=heading,
                           data=data,
                           data_keys=data_keys,
                           for_paginator=for_paginator,
                           length_selector=length_selector,
                           link=link,
                           link_to_house=link_to_house)


@app.route('/addrobj/<objectid>', methods=['GET', 'POST'])
def addrobj(objectid):
    title = 'BOD | Address Object'
    heading = 'Address Object'
    data = Addrobj.get_data(objectid)

    return render_template('addrobj.html',
                           title=title,
                           heading=heading,
                           data=data)


# @app.route('/houses/<page>', methods=['GET', 'POST'])
# def houses(page):
#    title = 'My app - Address Objects'
#    heading = 'Address Objects'
#    # TO DO Выбирать length из селектора (12, 24, 48, 96)
#    length_selector = LengthSelector()
#    if request.method == 'POST':
#        length = LengthSelector().selector.data
#    else:
#        length = 0
#    default_length = 12
#    if length == 0:
#        length = default_length
#    for_paginator = [int(page)-1, int(page), int(page)+1]
#    link = '/addrobjs'
#    data = House_list.get_data(LENGTH=length, SKIP=length*int(page)-1)
#    data_keys = data.keys()
#    link_to_house = []
#    for s in data_keys:
#        link_to_house.append('/addrobj/' + s)
#
#    return render_template('addrobjs.html',
#        title=title,
#        heading=heading,
#        data=data,
#        data_keys=data_keys,
#        for_paginator=for_paginator,
#        link=link,
#        link_to_house=link_to_house,
#        length_selector=length_selector)


# @app.route('/house/<objectid>', methods=['GET', 'POST'])
# def house(objectid):
#    title = 'My app - Address Object'
#    heading = 'Address Object'
#    ADDROBJ_OBJECTID = objectid
#    data = House.get_data(ADDROBJ_OBJECTID)
#
#    return render_template('addrobj.html',
#        title=title,
#        heading=heading,
#        data=data)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    users = bod_users.get_collection('users')
    form = LoginForm()
    title = 'My app - Login'
    heading = 'Log in'
    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html',
                           title=title,
                           heading=heading,
                           form=form,
                           users=users)


@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    mes = ''
    users = bod_users.get_collection('users')
    form = RegisterForm()
    title = 'My app - Sign up'
    heading = 'Sign up'
    if form.validate_on_submit() and users.find_one({'username': form.username.data}) is None:
        users.insert_one({'username': form.username.data,
                         'password': form.password1.data})
        return redirect(url_for('index'), title=form.username.data)
    else:
        mes = 'Пользователь с таким именем уже существует'

    return render_template('signup.html',
                           title=title,
                           heading=heading,
                           form=form,
                           mes=mes)


# @app.route('/map')
# def map():
#    title = 'My app - Map'
#    heading = 'Map'
#    return render_template('map_v2.html',
#        title=title,
#        heading=heading)


@app.route('/map')
def map():
    # title = 'My app - Map'
    # heading = 'Map'
    fol_map = folium.Map(location=[54.217044, 49.603082],
                         zoom_start=12,
                         zoom_control=False,
                         width='100%',
                         height='100%',
                         left='0',
                         top='0',
                         position='sticky',
                         )
    fol_map.save('app/templates/map_generated.html')
    # pos = fol_map.get_bounds.....
    title = 'My app - Map'
    return render_template('map_v3.html', title=title)
