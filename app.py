import os
from flask import Flask, jsonify, request, flash, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import imghdr


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, decode_token
)
from flask_jwt_extended.exceptions import JWTDecodeError, CSRFError
from flask_wtf.csrf import CSRFProtect
from functools import wraps
import datetime

from controller import blogger_controller, news_controller, featured_image_controller
from entertainment_model import blogger_model, news_model, featured_image_model


# Retrieves database configuration from environment variables
mysql_host = os.environ.get('MYSQL_HOST')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
db_name = os.environ.get('DB_NAME')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 1024*500       #Maximum file upload sixe is 1MB

# App flask Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + mysql_user + ':' + mysql_password + '@' + mysql_host + '/' + db_name
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  #The Jwt_secret_key is obtained from environment variables
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


b_controller = blogger_controller.BloggerController(db)     #Create instance of blogger controller to perform some operations
n_controller = news_controller.NewsController(db)     #create instance of news controlloer to perform some operations
f_controller = featured_image_controller.FeaturedImageController(db) # creates instance of featured iamge controller to perform some operations



# Register a blogger
@app.route('/bloggers/register', methods=['POST'])
def register():
    try:
            # Gets all input data from the user
        user_name = request.form.get('user_name')
        surname = request.form.get('surname')
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')     

        # Checks to see if the entry email is in the database. If not, it returns None
        getemail = b_controller.get_email(email)

        if getemail == None:   # If email is not already registered, input the data into the database
            b_controller.add_blogger(blogger_model.Blogger(user_name, surname, first_name, email, password))
            return {'success': 'succesfully updated in the database'}

        elif email == getemail[0]:  # If email is already used, notify the user
            return {'Error': 'This email has already been used to register'}

    except:
        return {'Error': 'Unable to Register'}

#validates to check if the image is indeed an image
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return (format if format != 'jpeg' else 'jpg')


#This route is to return the image from the local storage.
@app.route('/uploads/blogimage/<yr>/<mn>/<dy>/<filename>', methods=['GET'])
def get_blogimage(yr, mn, dy, filename):
    return send_from_directory((os.path.join(app.config['UPLOAD_PATH'], 'blogimage', str(yr), str(mn), str(dy))), filename)


#This route is to upload a blog image
@app.route('/blogimage', methods=['POST'])
@jwt_required
def uploadblogimage_file():
    uploaded_file = request.files['file']
    ts = int(datetime.datetime.now().timestamp())
    date = datetime.datetime.fromtimestamp(ts)

    yr = date.year
    mn = date.month
    dy = date.day

    filename = secure_filename(uploaded_file.filename)

    if filename != '':
        name = filename.split('.')[0]
        file_ext = filename.split('.')[1]
        
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            abort(400, description="File format not supported")

        filename = name + str(ts) + '.' + file_ext

        try:   
            if os.path.isdir('./uploads/blogimage/' + str(yr) + '/' + str(mn) + '/' + str(dy)) is True:
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], 'blogimage', str(yr), str(mn), str(dy), filename))

            else:
                directory = './uploads/blogimage/' + str(yr) + '/' + str(mn) + '/' + str(dy)
                print(directory)
                os.makedirs(directory)  
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], 'blogimage', str(yr), str(mn), str(dy), filename))

            stat = 'upload successful'             #Default status if file upload is successful 
            link = 'http://127.0.0.1:5000/uploads/blogimage/' + str(yr) + '/' + str(mn) + '/' + str(dy) + '/' + str(filename)

        except:
            stat = 'upload not succesful'
            link = 'no link returned because upload was unsuccessful'
         
               
        return {'status':stat, 'link': link}




#This route is to get a featured image
@app.route('/uploads/featuredimage/<yr>/<mn>/<dy>/<filename>', methods=['GET'])
def get_featuredimage(yr, mn, dy, filename):

    return send_from_directory((os.path.join(app.config['UPLOAD_PATH'], 'featuredimage', str(yr), str(mn), str(dy))), filename)


#This route is to upload a featured image
@app.route('/featuredimage', methods=['POST'])
@jwt_required
def uploadfeaturedimage_file():
    uploaded_file = request.files['file']
    ts = int(datetime.datetime.now().timestamp())
    date = datetime.datetime.fromtimestamp(ts)

    yr = date.year
    mn = date.month
    dy = date.day

    filename = secure_filename(uploaded_file.filename)

    if filename != '':
        name = filename.split('.')[0]
        file_ext = filename.split('.')[1]
        
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            abort(400, description="File format not supported")

        filename = name + str(ts) + '.' + file_ext

        try:   
            if os.path.isdir('./uploads/featuredimage/' + str(yr) + '/' + str(mn) + '/' + str(dy)) is True:
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], 'featuredimage', str(yr), str(mn), str(dy), filename))

            else:
                directory = './uploads/featuredimage/' + str(yr) + '/' + str(mn) + '/' + str(dy)
                print(directory)
                os.makedirs(directory)  
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], 'featuredimage', str(yr), str(mn), str(dy), filename))

            stat = 'upload successful'             #Default status if file upload is successful 
            link = 'http://127.0.0.1:5000/uploads/featuredimage/' + str(yr) + '/' + str(mn) + '/' + str(dy) + '/' + str(filename)

        except:
            stat = 'upload not succesful'
            link = 'no link returned because upload was unsuccessful'
         
               
        return {'status':stat, 'link': link}

#This route is to post news
@app.route('/api/news', methods=['POST'])
@jwt_required
def post_news():
    user = get_jwt_identity()
    user_id = int(user['id'])
    ts = datetime.datetime.now()
    ts = str(ts)
    try:
        # Gets all input data from the user
        title = request.form.get('title')
        news = request.form.get('news')
        fi = request.form.get('featured_image') # gets featured image
      
    except:
        return {'Error': 'Unable to retrieve news details'}

    print(news, fi, ts)
    
    try:
        n_controller.add_news(news_model.News(user_id, title, news, ts))  #Save news in the database  
        
        if fi != '':
            news_id = n_controller.get_news_id(user_id, ts)     # return the news_id
            f_controller.add_featured_image(featured_image_model.FeaturedImage(news_id, fi))
    except:
        return {'Error': 'Unable to upload news'}

    return {'success': 'News has been updated'}
    

#This route is to get news in a news page
@app.route('/api/newslist/<int:per>/<int:page_num>', methods=['GET'])   #per means the number per page and page_num means the page number
@jwt_required
def get_news_list(per, page_num):

    if page_num == 0:
        page_num = 1

    if per == 0:
        per = 20

    threads = db.session.query(news_model.News).paginate(per_page = per, page = page_num, error_out=False)
    no_of_items = len(threads.items)

    news = {}
    status = 'failed'
    
    if no_of_items > 0:
        for a in range(no_of_items):
            blogger_id = threads.items[a].blogger_id
            blogger_name = b_controller.blogger_name(blogger_id)
            news.update({threads.items[a].id: {'news_id':threads.items[a].id, 'blogger_id': blogger_name, 'title': threads.items[a].title}})

        status = 'success'

    news_list = {'news_list': news, 'status':status}

    print("i'm here")

    return news_list


#This route is to get the info in a specific news based on the news_id
@app.route('/api/news/<int:news_id>', methods=['GET'])  
@jwt_required
def get_news(news_id):   

    try:  
        news_object = n_controller.get_news(news_id)
        blogger_id = news_object.blogger_id
        blogger_name = b_controller.blogger_name(blogger_id)
        content = news_object.content
        title = news_object.title
        ts = news_object.timestamp
        status = 'success'

        news = {'blogger_name': blogger_name, 'title': title, 'content': content, 'time': ts}

    except:
        news = 'Record not found'
        status = 'failed'

    return {'status': status, 'news':news}


# Function to login
@app.route('/token/auth', methods=['POST'])
def login():
    
    try:
        # Gets email and password inputed by the user
        email = request.form.get('email')
        pass_word = request.form.get('password')

    
            # Checks if email has been registered. If this line fails, it runs the except block
        password = b_controller.get_password(email)
        # Checks if password is correct
        if bcrypt.check_password_hash(password[0], pass_word):
            user_name = b_controller.get_user_name(email)
            blogger_id = b_controller.get_blogger_id(email)

            access_token = create_access_token(identity={'User name': user_name[0], 'id': blogger_id[0]}, expires_delta=datetime.timedelta(days=1))
            refresh_token = create_refresh_token(identity={'User name': user_name[0], 'id': blogger_id[0]}, expires_delta=datetime.timedelta(days=1))

            resp = jsonify({'refresh': True, 'user name': user_name[0]})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
        else:
            return jsonify({'login': False}), 401

    except Exception as e:
        return jsonify({'login': False}), 401

    


if __name__ == '__main__':
    app.run(debug=True)
