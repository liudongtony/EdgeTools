## Description


## How to run
1. Set environment argument

2. setup virtual environment: pip install -r requirements.txt

3. Start server for dev

    3.1 In Pycharm: Run -> Edit Configuration ... -> Script parameters: runserver --host 0.0.0.0
    
    3.2 In terminal: python edgeTools.py runserver --host 0.0.0.0

4. init db: python manage.py shell  --> from manage import db
--> db.drop_all() --> db.create_all() --> from app.models import Role, User
--> user_role = Role(name='User') --> user_john=User(username='john', role=user_role)
db.session.add_all([user_role, user_john]) --> db.session.commit()

5. unittest coverage: python manage.py test --coverage


    
