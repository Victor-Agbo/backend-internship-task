# Submission


## Commands to Set Up

- Install Requirements

`pip install -r requirements.txt`

- Migrate Database

`python manage.py makemigrations`

`python manage.py migrate`

- Create SuperUser
> This is need to assign users high roles and permissions

`python manage.py createsuper` , then follow the prompts

- Migrate Database... again

`python manage.py makemigrations`

`python manage.py migrate`

## Command to run the test suite

`python manage.py test`

## Command to run the API server

`python manage.py runserver`