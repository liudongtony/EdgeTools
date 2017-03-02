## Description
Learn from here: https://github.com/miguelgrinberg/flasky.git

## How to run
1. Set environment argument
export FLASKY_ADMIN="testofdong@gmail.com"

2. setup virtual environment: pip freeze requirements/dev.txt  --> pip install -r requirements/dev.txt
or on server
CentOs upgrade Python: http://ruter.sundaystart.net/2015/12/03/Update-python/
$ sudo yum install python-virtualenv --> virtualenv venv -->  $ source venv/bin/activate  --> (venv)../flasky $ deactivate
Run gunicorn:  sudo gunicorn -b 0.0.0.0:80 manage:app -p gunicorn.pid -D  -->kill 'cat gunicorn.pid'

3. Start server for dev

    3.1 In Pycharm: Run -> Edit Configuration ... -> Script parameters: runserver --host 0.0.0.0
    3.2 In terminal: python manage.py runserver --host 0.0.0.0 

4. init db: python manage.py shell  --> from manage import db
--> db.drop_all() --> db.create_all() 

insert 3 roles: --> Role.insert_roles()
insert some fake data: python manage.py shell  --> User.generate_fake(10)  
shell --> from app.models import Post --> Post.generate_fake(100)

5. unittest coverage: python manage.py test --coverage

6. database migration: python manage.py db init  --> python manage.py db migrate -m 'xxx' -->python manage.py db upgrade

7. Unittest: python manage.py test --coverage

8. selenium: upgrade firefox --> download geckodriver (https://github.com/mozilla/geckodriver/releases) and copy to /usr/local/bin


## Learn Flask
{{ url_for('auth.reset_password_request') }} --> Find in views.py --> 
@auth.route('/resetpassword', methods=['GET', 'POST'])
def reset_password_request():


    
