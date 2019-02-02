from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from database import Base, Cheese, CheeseItem, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import string
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response
from functools import wraps


app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').
                       read())['web']['client_id']
APPLICATION_NAME = "cheese-world"

engine = create_engine('sqlite:///cheesewithuser.db',
                       connect_args={'check_same_thread': False}, echo=True)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# creating login session.
@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# creating gconnect method.
@app.route('/gconnect', methods=['POST'])
def gconnect():
        if request.args.get('state') != login_session['state']:
            response = make_response(json.dumps('Invalid state'
                                     'parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        code = request.data
        try:
            ''' Transfer authorization code into a credentials object'''
            oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                                 scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(code)
        except FlowExchangeError:
            response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid or not.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify the access token.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = make_response(
                json.dumps("Token's user ID doesn't"
                           "match given user ID."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify the access token is valid for the app.
        if result['issued_to'] != CLIENT_ID:
            response = make_response(json.dumps("Token's client ID does not"
                                                "match app's."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        stored_access_token = login_session.get('access_token')
        stored_gplus_id = login_session.get('gplus_id')
        if stored_access_token is not None and gplus_id == stored_gplus_id:
            response = make_response(json.dumps('Current user is'
                                                'already connected.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Store the access token in the session.
        login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        login_session['username'] = data['name']
        login_session['email'] = data['email']
        login_session['provider'] = 'google'

        # Check if the user is exist or not.
        user_id = getUserID(login_session['email'])
        if not user_id:
            user_id = createUser(login_session)
        login_session['user_id'] = user_id
        output = ''
        output += '<h1>Welcome, '
        output += login_session['username']
        output += '!</h1>'
        flash("you are now logged in as %s" % login_session['username'])
        print "done!"
        return output


# creating new user.
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# getting user info.
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# getting user ID.
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# disconnect from connected user.
@app.route("/glogout")
def gdisconnect():
        access_token = login_session.get('access_token')
        if access_token is None:
            response = make_response(json.dumps('Current user not'
                                     'connected.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
               % access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        if result['status'] == '200':
            # Reset the user's sesson.
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']

            response = make_response(json.dumps('Successfully'
                                                'logged out!.'), 200)
            response.headers['Content-Type'] = 'application/json'
            flash('Successfully Logged Out!')
            return redirect(url_for('cheesecountry'))

        else:
            # For whatever reason, the given token was invalid.
            response = make_response(json.dumps('Failed to revoke'
                                     'token for given user.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response


# showing in JSON file with specfic country name and its items present in it.
@app.route('/cheese/<int:cheese_id>/JSON')
def cheeseJSON(cheese_id):
    cheese = session.query(Cheese).filter_by(id=cheese_id).all()
    item = session.query(CheeseItem).filter_by(cheese_id=cheese_id).all()
    return jsonify(Cheese=[i.serialize
                   for i in cheese], Items=[i.serialize for i in item])


# Login Required function.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


# show cheese country.
@app.route('/')
def cheesecon():
    cheese = session.query(Cheese)
    if 'username' not in login_session:
        return render_template('public.html', cheese=cheese)
    else:
        return render_template('showcountry.html', cheese=cheese)


# display cheese country.
@app.route('/cheese/')
def cheesecountry():
    cheese = session.query(Cheese)
    if 'username' not in login_session:
        return render_template('publiccheese.html', cheese=cheese)
    else:
        return render_template('country.html', cheese=cheese)


# add cheese country.
@app.route('/cheese/addcheese/', methods=['GET', 'POST'])
@login_required
def addcheesecon():
    if request.method == 'POST':
        newch = Cheese(name=request.form['name'],
                       user_id=login_session['user_id'])
        user_id = login_session['user_id']
        session.add(newch)
        session.commit()
        flash('Cheese country Successfully Added!')
        return redirect(url_for('cheesecountry'))
    else:
        return render_template('addcheesecon.html')


# Edit a cheese country.
@app.route('/cheese/<int:cheese_id>/edit', methods=['GET', 'POST'])
@login_required
def editcheesecon(cheese_id):
    editedch = session.query(Cheese).filter_by(id=cheese_id).one()
    c = session.query(Cheese).filter_by(id=cheese_id).one()
    creator = getUserInfo(editedch.user_id)

    if 'username' in login_session:
        if login_session['user_id'] == editedch.user_id:

            # POST methods.
            if request.method == 'POST':
                if request.form['name']:
                    editedch.name = request.form['name']
                session.add(editedch)
                session.commit()
                flash('Cheese country name Successfully Edited!')
                return redirect(url_for('cheesecountry'))
            else:
                return render_template('editcheesecon.html',
                                       cheese_id=cheese_id, ch=editedch)

        else:
            flash('premission denied as it belongs to %s' % creator.name)
            return redirect(url_for('cheesecountry'))

    else:
        return redirect('/login')


# Delete a cheese country.
@app.route('/cheese/<int:cheese_id>/delete', methods=['GET', 'POST'])
@login_required
def deletecheesecon(cheese_id):
    chDelete = session.query(Cheese).filter_by(id=cheese_id).one()
    creator = getUserInfo(chDelete.user_id)

    if 'username' in login_session:
        if login_session['user_id'] == chDelete.user_id:

            if request.method == 'POST':
                session.delete(chDelete)
                session.commit()
                flash('Cheese Successfully Deleted!')
                return redirect(url_for('cheesecountry'))
            else:
                return render_template('deletecheesecon.html', i=chDelete)
        else:
            flash('premission denied as it belongs to %s' % creator.name)
            return redirect(url_for('cheesecountry'))

    else:
        return redirect('/login')


# Display cheese items.
@app.route('/cheese/<int:cheese_id>/display')
def cheesemenu(cheese_id):
    cheese = session.query(Cheese).filter_by(id=cheese_id).one()
    item = session.query(CheeseItem).filter_by(cheese_id=cheese.id)
    return render_template('showcheeseall.html',
                           cheese=cheese, item=item)


# shows cheese items.
@app.route('/cheese/<int:cheese_id>/')
def cheeseMenu(cheese_id):
    cheese = session.query(Cheese).filter_by(id=cheese_id).one()
    item = session.query(CheeseItem).filter_by(cheese_id=cheese.id)
    return render_template('showcheese.html',
                           cheese=cheese, item=item)


# Adding new cheese item.
@app.route('/cheese/<int:cheese_id>/new/', methods=['GET', 'POST'])
@login_required
def newcheeseType(cheese_id):
    cheese = session.query(Cheese).filter_by(id=cheese_id).one()
    creator = getUserInfo(cheese.user_id)
    if 'username' in login_session:
        if login_session['user_id'] == cheese.user_id:
            if request.method == 'POST':
                newItem = CheeseItem(name=request.form['name'],
                                     description=request.form['desp'],
                                     price=request.form['price'],
                                     cheese_id=cheese_id,
                                     user_id=login_session['user_id'])
                session.add(newItem)
                session.commit()
                flash("new cheese items created!")
                return redirect(url_for('cheeseMenu', cheese_id=cheese_id))
            else:
                return render_template('newcheeseitem.html',
                                       cheese_id=cheese_id)
        else:
            flash('premission denied as belongs to %s' % creator.name)
            return redirect(url_for('cheeseMenu', cheese_id=cheese_id))
    else:
        return redirect('/login')


# Edit cheese item.
@app.route('/cheese/<int:cheese_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editcheeseItem(cheese_id, item_id):
    editedItem = session.query(CheeseItem).filter_by(id=item_id).one()
    creator = getUserInfo(editedItem.user_id)

    if 'username' in login_session:
        if login_session['user_id'] == editedItem.user_id:
            if request.method == 'POST':

                if request.form['name']:
                    editedItem.name = request.form['name']
                session.add(editedItem)
                session.commit()
                flash("cheese item edited!")
                return redirect(url_for('cheeseMenu', cheese_id=cheese_id))
            else:
                return render_template('editcheeseitem.html',
                                       cheese_id=cheese_id,
                                       item_id=item_id,
                                       i=editedItem)
        else:
            flash('premission denied as belongs to %s' % creator.name)
            return redirect(url_for('cheeseMenu', cheese_id=cheese_id))

    else:
        return redirect('/login')


# Delete cheese item.
@app.route('/cheese/<int:cheese_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deletecheeseItem(cheese_id, item_id):
    itemDelete = session.query(CheeseItem).filter_by(id=item_id).one()
    creator = getUserInfo(itemDelete.user_id)

    if 'username' in login_session:
        if login_session['user_id'] == itemDelete.user_id:

            if request.method == 'POST':
                session.delete(itemDelete)
                session.commit()
                flash("cheese item deleted!")
                return redirect(url_for('cheeseMenu', cheese_id=cheese_id))
            else:
                return render_template('deletecheese.html', i=itemDelete)
        else:
            flash('premission denied as belongs to %s' % creator.name)
            return redirect(url_for('cheeseMenu', cheese_id=cheese_id))

    else:
        return redirect('/login')
    return


# main method.
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
