This is the Entertainment API
To setup:
1) Run the requirement.txt file
2) Set the environment variables for :
    a) mysql_host
    b) mysql_password
    c) mysql_user
    d) db_name - (Database name)
    e) jwt_secret_key

This Entertainment API can do 14 major things:
1) Register a blogger
2) Login 
3) upload a blog image
4) get a blog image
5) upload a featured image
6) get a featured image
7) Post a news
8) Get the list of news in a page
9) Get a specific news details
10) Like a news
11) Unlike a news
12) retrieve likes
13) comment on a news
14) retrieve comments



1) REGISTER A BLOGGER
To register a new blogger, you use the route '/bloggers/register'. This is a Post request
The  general user data that are required include:
a) user_name 
b) surname
c) first_name 
d) email 
e) password

Sample input data:
user_name  : Emmapopo
surname    : Oyedeji
first_name : Emmanuel
email      : emmanueloyedeji20@yahoo.com
password   : Abayomi20

If input is successful, it returns :                                         {'success': 'succesfully updated in the database'}
If email has been used to register before, it returns:                       {'Error': 'This email has already been used to register'}
If any of the input does not conform to the expected datatype, it returns:   {'Error': 'Unable to Register'}  



2) LOGGING IN
LOGIN AS A USER
To login, you just need to supply two information in the POST request. The path is '/token/auth':
(a) email
(b) password

Sample 
http://localhost/token/auth
email: emmanueloyedeji20@yahoo.com
password: Popo1234

If login detaials are valid, it returns: "refresh": true,
                                        "user name": "popo1"
            
If either the email or password is wrong, it returns:  "login": false



3) UPLOAD A BLOG IMAGE
Uploading a blog image is a POST request. The path is '/blogimage'

The only information is send is:
a) uploaded_file

A sample request is
http://127.0.0.1:5000/blogimage
uploaded_file : <upload the image file>  

The uploaded file must adhere to the following restrictions:
format: {'png', 'jpg', 'jpeg'}
size: 500kb

If the uploaded file is valid, it returns: 
{
  "link": "http://127.0.0.1:5000/uploads/blogimage/2020/8/21/Sketchpad1598030155.png",
  "status": "upload successful"
}

If an unaccepted format is used, it returns a 404 error, Bad Request, File Format Not Supported
If the file size limit is exceeded, it returns a 404 error, Bad Request, File Size Limit Exceeded.
If upload is unsuccesful, it returns:
'stat':'upload not succesful'
'link':'no link returned because upload was unsuccessful'



4) GET A BLOG IMAGE
This is a GET request: The path is ''/uploads/blogimage/<yr>/<mn>/<dy>/<filename>'
where:
yr = year
mn = month
dy = day
filename = file of the name:

Here is a sample get request to get a blog image:
http://127.0.0.1:5000/uploads/blogimage/2020/8/21/Sketchpad1598030155.png

If successful, it returns the image
If it fails, it returns a 404 error, File Not Found.



5) UPLOAD A FEATURED IMAGE
Uploading a featured image is a POST request. The path is '/featuredimage'

The only information is send is:
a) uploaded_file

A sample request is
http://127.0.0.1:5000/featuredimage
uploaded_file : <upload the image file>  

The uploaded file must adhere to the following restrictions:
format: {'png', 'jpg', 'jpeg'}
size: 500kb

If the uploaded file is valid, it returns: 
{
  "link": "http://127.0.0.1:5000/uploads/featuredimage/2020/8/21/Sketchpad1598030744.png",
  "status": "upload successful"
}

If an unaccepted format is used, it returns a 404 error, Bad Request, File Format Not Supported
If the file size limit is exceeded, it returns a 404 error, Bad Request, File Size Limit Exceeded.
If upload is unsuccesful, it returns:
'stat':'upload not succesful'
'link':'no link returned because upload was unsuccessful'



6) GET A FEATURED IMAGE
This is a GET request: The path is '/uploads/featuredimage/<yr>/<mn>/<dy>/<filename>'
where:
yr = year
mn = month
dy = day
filename = file of the name:

Here is a sample get request to get a featured image:
http://127.0.0.1:5000/uploads/featuredimage/2020/8/21/Sketchpad1598030744.png

If successful, it returns the image
If it fails, it returns a 404 error, File Not Found.



7) POST A NEWS
This is a POST request. The path is '/api/news'

To upload a news, you must first be logged in:
Here are the required information:
a) title
b) news 
c) featured_image : The faetured image is the link to the featured image

Here is a sample input:
title          :    Farm
news           :    A farm is an area of land and its buildings, used for growing crops and rearing animals.
featured_image :    http://127.0.0.1:5000/uploads/featuredimage/2020/8/21/Sketchpad1598030744.png

If the news upload is succesful, it returns: 
{
  "success": "News has been updated"
}

If the form field is wrong, it returns          :         {'Error': 'Unable to retrieve news details'}
If it is unable to uplaod the news, it returns  :         {'Error': 'Unable to upload news'}



<!-- 8) GET THE LIST OF NEWS ON A PAGE
This is GET request that allows the user to get a list of news on a page.
The route is: '/api/newslist/<int:per>/<int:page_num>'
where:
per is the number of news list required in a page
page_num is the specific page number

Here is a sample a request:
Link: http://127.0.0.1:5000/api/newslist/2/2
And here is the return:
{
  "news_list": {
    "3": {
      "blogger_id": "Daniel Adewuyi",
      "news_id": 3,
      "title": "boy"
    },
    "4": {
      "blogger_id": "Daniel Adewuyi",
      "news_id": 4,
      "title": "Farm"
    }
  },
  "status": "success"
}

If no news list is returned for the request, it returns:
{
  "news_list": {},
  "status": "failed"
}



9) GET A SPECIFIC NEWS DETAILS
This is a GET request. 
The route is: '/api/news/<int:news_id>'
where:
news_id is the news id:

Here is a sample request:
http://127.0.0.1:5000/api/news/1

If the request is succesful, it returns:
{
    "1": {
        "blogger_name": "Monihan Patrick",
        "content": "Bouyuhs hasudch hiuukdhnjck hiudjc",
        "featured image": "http://127.0.0.1:5000/uploads/blogimage/2020/12/21/WIN_20201208_12_24_49_Pro1608560765.jpg",
        "no of comments": 0,
        "no of likes": 1,
        "time": "Sat, 30 Jan 2021 16:02:50 GMT",
        "title": "boy",
        "user like ?": "no"
    },
    "status": "success"
}

If the news id doesn't exist, it returns:
{
  "news": "Record not found",
  "status": "failed"
}


10) LIKE A NEWS
This is a POST request. The path is '/api/news/like'

The information that needs to be provided are:

a) news_id

A sample request is
http://127.0.0.1:5000/api/news/like
news_id: 1

if successful, it returns:
{
    "status": "liked"
}

If unsuccessful, it returns:
{
    "Error": "unable to like news"
}


11) UNLIKE A NEWS
This is a POST request. The path is '/api/news/unlike'

The information that needs to be provided is:
a) news_id

A sample request is
http://127.0.0.1:5000/api/news/unlike
news_id: 1

If successful, it returns,
{
    "status": "unliked"
}

If unsuccessful, it returns,
{
    "Error": "unable to unlike news"
}



12) RETRIEVE LIKES
This is a GET request.
The route is: '/api/likes/<news_id>'
where:
news_id is the news id:

Here is a sample request:
http://127.0.0.1:5000/api/likes/1

This means retrieve all the likes for news_id 1

If successful, it returns,
{
    "1": {
        "liker": 1,
        "timestamp": "Mon, 01 Feb 2021 13:26:10 GMT"
    },
    "6": {
        "liker": 2,
        "timestamp": "Mon, 01 Feb 2021 15:17:54 GMT"
    }
}

where "1" and "6" represents the like_id in the like table. 

If there are no likes, it returns
{}


13) COMMENT ON A NEWS
This is a POST request. The path is '/api/news/comment'

The information that needs to be provided is:
a) news_id
b) comment

A sample request is
http://127.0.0.1:5000/api/news/comment
news_id: 1
comment: 'Fuck all the things that are happening'

If successful, it returns:
{
    "status": "commented"
}

If unsuccessful, it returns:
{
    "Error": "unable to comment on news"
}


14) RETREIVE COMMENTS
This is a GET request.
The route is: '/api/comments/<news_id>'
where:
news_id is the news id:

Here is a sample request:
http://127.0.0.1:5000/api/comments/2

This means retrieve all the comments for news_id 2

If successful, it returns:
{
    "1": {
        "comment": "God save us from all this rubbish",
        "commenter": 2,
        "timestamp": "Mon, 01 Feb 2021 13:36:31 GMT"
    },
    "2": {
        "comment": "What's the meaning of all this rubbish again",
        "commenter": 2,
        "timestamp": "Mon, 01 Feb 2021 13:37:25 GMT"
    }
}

If there are no comments to be retrieved, it returns:
{}

 -->
