# Library Management System

The project aims at building a web application with `Django Framework` that confirms with the following specs -

- Authenticating the user with either admin or student account.
- Admin can add books, issue new books, view students, added and issued books.
- Student can view issued books and return them.

## Pre-Requisites

- Python v3.8 should be installed on your system
- Django Framework should be installed on your system
- Basic understanding of HTML, CSS, JS
- PIP Packages should be installed on your system

## Technology Stack

**Frontend**

- HTML
- CSS


**Backend**

- Django
- Python 3.8

  **Database**

- SqLite3

## Installing Dependencies

To run the app locally follow the below steps :

- Clone the repository.

```
git clone https://github.com/purvimandot/Library_DBMS.git
```


- To Make `migrations` to the database:

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations library
python3 manage.py migrate library
```


## Starting the Project

- Start the project using -

```
python3 manage.py runserver
```

- Browse to http://127.0.0.1:8000/ to see your web app.








