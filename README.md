# Students Houses App
**A Harry Potter themed point tracker application written in Python!**

## Several things to Note:
Old test PostgreSQL databse information will no longer be valid upon completion of this application. Proper configuration files will hide all database information in commits made after v1.0

## Installation:
In order for all of the modules (tkinter.ttk, psycopg2, etc) to work across all Operating Systems, please have Python 3.7.x and later installed. You can install it here:[Official Python Downloads](https://www.python.org/downloads/)

## Setting up the database:
Since the database schema was created inside a SQL IDE, specfically the PopSQL client, one can recreate the database table with the following SQL statements:
```
/*Drop table if it exists. Always run before creating new table*/
DROP TABLE IF EXISTS students;

/*Create table*/
CREATE TABLE students (
    pk SERIAL PRIMARY KEY,
    student_id INT,
    name VARCHAR(50),
    house VARCHAR(50),
    points INT
);
```
For more information on how to install and use PopSQL, please check out [PopSQL Documentation](https://popsql.com/docs/)

## Running the application:

### MacOS & Linux Distributions
Download the project folder, drag and drop it from Downloads to **Desktop**. If the folder is in a zipped state, unzip it by double clicking the folder. Then, open **Terminal**. You can also clone this repository directly to your Desktop by running 
```
cd ~/Desktop && git clone https://github.com/jmespana83/student-rewards-app.git
```
From **Terminal**, type in `cd ~/Desktop/student-rewards-app` and Enter. Once inside the folder, run the program by typing inside the Terminal:
```
python tigers_houses.py
```
and Enter. The program should automatically launch.

### IDE: All Systems
If you have a Python IDE installed, you can simply open **tigers_houses.py** inside the IDE and click `Run`.

## Heroku Deployment:
The web view is currently hosted on Heroku.
To create a heroku application, user must have a [Heroku account](https://signup.heroku.com/) and the [Heroku CLI installed locally](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

I perfomed the following steps below in the directory `students-reward-app/web/heroku/`

### Creating a simple PHP Application in Heroku.

This Heroku setup follows a tutorial from this [link](https://scotch.io/@phalconVee/deploying-a-php-and-mysql-web-app-with-heroku) (the example given was done on a Windows computer). However, my commands will be Mac/Linux specific and may have a lot of overlap with the above tutorial. If you're on a Windows computer, please use the **Git Bash** terminal.

Create a new project folder on your Desktop and change to that directory from your terminal.
```
mkdir my-heroku-project
cd Desktop
cd my-heroku-project
``` 
Inside that new folder, copy over the following files from web: **index.php**, **styles.css**,  **bootstrap.min.css**, and **roland-losslein-DmDYX_ltI48-unsplash.jpg**.
Then, intiate the current directory as a local git repository.
```
git init
```
Add all files to the staging area and commit it to your local master branch.
```
git add .               
git commit -m 'My first commit.'
```
Log into heroku. The command will open a link in a browswer for you to log in with your Heroku account.
```
heroku login
```
Then create a Heroku app and connect it to the current directory/repository. A link to the application will be provided to you in the console output. You can also find this link in your Heroku dashboard on the website.
```
heroku create
```
Deploy the App!
```
git push heroku master
```
When making code changes (like changing the database connections in the PHP file) and and re-deploying, make your code changes and just start from `git add .` and work through the steps, **BUT** skip `heroku create`.
