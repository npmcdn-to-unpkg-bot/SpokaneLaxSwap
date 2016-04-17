# This app is a prototype for spokane lacrosse swap, a craigslist type 
# website for lacrosse gear in the greater spokane area
####################### Imports ######################
from flask import Flask, render_template, request, redirect, make_response, flash, send_from_directory, jsonify
from flask import session as login_session

from werkzeug import secure_filename

from functools import wraps

import os
import base64
import httplib2
import json
import random, string
import requests

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Posting, User

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


app = Flask(__name__)


############### sqlalchemy mumbo jumbo ###############
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


################# Context Processors #################
@app.context_processor
def inject_user():
    """ Automatically injects user info into all templates (base header) """
    return dict(session_email=session_email())
def session_email():
    """ if theres no session email, returns empty string """
    if 'email' in login_session:
        return login_session['email']
    return ''


##################### Decorators #####################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return decorated_function


################# Greeting/About Pages ################
@app.route('/')
def greetingPage():
    return render_template('greeting_page.html')

@app.route('/about')
def aboutPage():
    return render_template('about.html')


###################### Postings ######################
# Page for reading postings
@app.route('/postings')
def getPostings():
    postings = session.query(Posting).order_by("id desc")
    return render_template('postings.html', posts=postings, title='Posts')

# shows post belonging to user if logged in
@app.route('/postings/myposts')
@login_required
def getMyPosts():
    my_posts = session.query(Posting).filter_by(user_id=login_session['email']).order_by("id desc")
    return render_template('postings.html', posts=my_posts, title='My Posts')

# shows posts for a specific category
@app.route('/postings/<category>')
def getCategoryPosts(category):
    category_posts = session.query(Posting).filter_by(category=category).order_by("id desc")
    return render_template('postings.html', posts=category_posts, title=category)

# shows all posts in json format
@app.route('/postings/json')
def getPostsJson():
    postings = session.query(Posting).order_by("id desc")
    return jsonify(Posts=[e.serialize for e in postings])

# shows a single post in json format
@app.route('/postings/json/<int:post_id>')
def getPostJson(post_id):
    post = session.query(Posting).filter_by(id=post_id).one()
    return jsonify(Posts=[post.serialize])

# Page to create a posting
@app.route('/postings/create', methods=['GET','POST'])
@login_required
def createPost():
    # stores form data in database if method is post and post is valid
    if request.method == 'POST':
        if valid_post(request.form['title'], request.form['description'], 
            request.form['price']) == True:
            # if user does not upload pic it will be a default pic
            picture = 'default.jpg'
            if request.files['pic']:
                picture = upload_image(request.files['pic'])
            newPosting = Posting(title = request.form['title'], 
                description = request.form['description'],
                price = request.form['price'],
                category = request.form['category'],
                picture = picture,
                user_id = login_session['email'])
            session.add(newPosting)
            session.commit()
            return redirect('/postings')
        # if post is not valid render error
        else:
            error = "ERROR: one or more fields are invalid"
            return render_template('post_create.html', title = request.form['title'], 
                description = request.form['description'], price = request.form['price'], 
                error=error)
    # if method is not post, renders original template
    return render_template('post_create.html')

# Page to view an individual posting
@app.route('/postings/post/<int:post_id>')
def showPost(post_id):
    posting = session.query(Posting).filter_by(id=post_id).one()
    return render_template('post_page.html', posting=posting)

# Page to edit a posting
@app.route('/postings/edit/<int:post_id>', methods=['GET','POST'])
@login_required
def editPost(post_id):
    posting = session.query(Posting).filter_by(id=post_id).one()
    # ensures correct user is making changes
    if login_session['email'] != posting.user_id:
        return redirect('/')
    # if method is post, stores all post info
    if request.method == 'POST':
        if valid_post(request.form['title'], request.form['description'], 
            request.form['price']) == True:
            # if image in form, deletes old pic and uploads new
            if request.files['pic']:
                delete_image(posting.picture)
                posting.picture = upload_image(request.files['pic'])
            posting.title = request.form['title']
            posting.description = request.form['description']
            posting.price = request.form['price']
            posting.category = request.form['category']
            session.add(posting)
            session.commit()
            return redirect('/postings')
        # if post isnt valid, throws an error message and redirects to edit page
        else:
            error = "ERROR: one or more fields are invalid"
            return render_template('post_edit.html', posting=posting, error=error)
    # if method is get, shows you page to edit
    return render_template('post_edit.html', posting=posting)

# Page to delete a posting
@app.route('/postings/delete/<int:post_id>', methods=['GET','POST'])
@login_required
def deletePost(post_id):
    posting = session.query(Posting).filter_by(id=post_id).one()
    # ensures correct user is attempting to delete the post
    if login_session['email'] != posting.user_id:
        return redirect('/')
    # if method is post, post is deleted
    if request.method == 'POST':
        if posting != []:
            session.delete(posting)
            # makes sure we dont delete the default image
            delete_image(posting.picture)
            session.commit()
            return redirect('/postings')
    # if method is get renders confirmation page
    return render_template('post_delete.html', posting=posting)



### Some functions to help with post pages ###
def valid_post(title, description, price):
    """ Ensures the post fields are valid length """
    min_len = 2
    max_title_len = 30
    max_description_len = 400
    if len(title) > min_len and len(title) < max_title_len:
        if len(description) > min_len and len(description) < max_description_len:
            if price.isdigit():
                return True
    return False
    
def upload_image(image):
    """ uploads image to post_images folder and returns filename for db """
    filename = secure_filename(image.filename)
    image.save('static/post_images/%s' % filename)
    return filename

def delete_image(filename):
    if filename != 'default.jpg':
        os.remove('static/post_images/%s' % filename)
    return



##################### Login Stuff ####################
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Spokane Lax Swap"

### Some Functions ###
def create_user(login_session):
    """ Creates a new user in the database using login session info """
    new_user = User(name = login_session['username'], email = login_session['email'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def get_id(email):
    """ checks if user already exists in database, if so it returns their id """
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def get_info(user_id):
    """ retrieves user info using their id """
    user = session.query(User).filter_by(id = user_id).one()
    return user

@app.route('/login')
def showLogin():
    """ renders login page and injects state key """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    
    # If user is new, stores their info in the database
    try:
        user_search = session.query(User).filter_by(email = login_session['email']).one()
    except:
        create_user(login_session)

    return login_session['email']

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

###################################################
if __name__ == '__main__':
    app.secret_key = "kBbo3WmsA71an6TBaO54o1Mx"
    app.debug=True
    app.run(host='0.0.0.0', port=5000)