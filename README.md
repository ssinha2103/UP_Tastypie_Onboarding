# UP_onboarding_project

# Introduction

The goal of this project is to provide minimalistic django project on:-

• A Web App 
• Database 
• RESTful API endpoints for: 
• Creating merchants, stores and items 
• APIs should handle list view, detail view, CRUD operations 
• Authentication! 
• Test-cases 

### Techs Used

- `Django`
- `TastyPie`
- `SQLite3`

      
### Steps To Reciprocate


Installing inside virtualenv is recommended, however you can start your project without virtualenv too.



# Getting Started

    
Activate the virtualenv for your project.


Add .env file to the project folder with a Django Security Key:


Create a MySQL database with name `up-task` and update the username and password in settings of project directory.

    
Install project dependencies:

    $ pip install -r requirements.txt
    

Then simply make the migrations:

    $ python manage.py makemigrations
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver


### Endpoints for Now

- `/admin/` It opens the admin page for the Django app.
- `/register/` For registering users on the basis of Role that are Merchant and Consumer.
- `/user/login/` For logging in as Merchant or Consumer.
- `'/user/logout/'` For logging out as Merchant or Consumer.
- `/profiles/` Can be used by anyone to view the Users registered.
- `/stores/` Used by Merchant for adding a new and view their registered stores.
- `/items/` Used by Merchant for adding items under their Registered Stores.
- `/place_orders/` Used by consumer to place orders.
- `/see_orders/` Used used by the merchant to see the orders that have been placed that their registered stores.


### WEEK_1_Task - [Status-Done]
- A Web App 
- Database 
- RESTful API endpoints for: 
- Creating merchants, stores and items 
- APIs should handle list view, detail view, CRUD operations 
- Authentication! 
- Test-cases

- Technology Used [Virtualenv, Django, Pytest, Tastypie, SQLite3, Github workflow]
