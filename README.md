Synopsis
========
This project is a submission for my Stage 3 projects of the Full Stack Developer Nanodegree through Udacity. It is a Craigslist type website for lacrosse gear in the Spokane Area, using full CRUD functionality as well as API endpoints (JSON)


How to Run
==========
Run the main.py file using vagrant. 
If you wish to automatically populate the database, you can do so by running the database_populator.py file.


Files
=====
main.py - runs the site  
database_setup.py - automatically run through main.py, initalizes the database  
database_populator.py - populates the database with sample posts, used for demo purposes only  
client_secrets.json - contains the secret for connecting with google+  
templates(folder) - stores html templates  
static(folder) - houses all static files and folders listed below:
  * post_images(folder) - stores all post images  
      * default.jpg - DO NOT DELETE, is the standard image used when user doesnt upload one  
      * postX.jpg - images used in sample posts created using database_populator  
  * site_images(folder) - contain images for the sites artwork  
      * header.jpg - site header image
