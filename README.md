# Cyber Security Project 1

This is my project for Cyber Security Project for https://cybersecuritybase.mooc.fi/module-3.1. My project includes the description and fixes for each flows according to OWASP 2017 top ten list.

My web application is about the handling of one/multiple bank account(s) for the users. The web application is very simple that allows user to create an account, top up the money and display the existing accounts (of the user) with the balance. 

The project is about showing the 5 types of vulnerabilities and fixes to them are commented out. 

## Installation Instructions

1. Clone the directory
2. Run the server with: ``python3 manage.py runserver``

You can use the three premade users:

- ``username: alice``
``password: redqueen``

- ``username: bob``
``password: squarepants``

If you want to create a new user, open up the terminal and go into this folder. Then, type ``python3 manage.py createsuperuser``. Then, you will be asked to enter new username, email and password. Only enter username and password while skipping email section by pressing enter button.

This will make the user as superuser status. To downgrade the status, type ``python3 manage.py shell``. 

```
from django.contrib.auth.models import User
Update Bob's superuser status
bob = User.objects.get(username='bob')
bob.is_superuser = False
bob.save()
Update Alice's superuser status
alice = User.objects.get(username='alice')
alice.is_superuser = False
alice.save()```


## Flaw 1: Broken Authentication
Broken authentication is defined as the application which lacks robust identification and authentication mechanisms. For instance, the password that are guessable, short or lacking in combination of digits, lower or upper alphabets are considered as weak password. To add on, users often use username as password for creating an account quickly. These issues need to be addressed because it is possible for attackers to crack the password. 



Fixes: are commented in the following sections.

## Flaw 2: SQL Injection
Another vulnerability is SQL injection when an attacker is able to manipulate a SQL query as shown in the code by injecting malicious SQL code in the web application. In my application, if an attacker somehow is capable of manipulating a SQL query and inserts his iban, instead of the iban account that user has chosen, an attacker gains the money instead of user who genuienely tops up the money. 

Fix: Instead of using traditional SQL query to update the database, Django's ORM or parameterized queries prevents this vulnerability.

## Flaw 3: Sensitive Data Exposure
Description : In the HTML form, there are mainly 2 ways of sending the form to the server. They are GET and POST methods. Both could serve same purposes while there is a difference between them. GET method should be used whenever the form does not include any sensitive data while opposite goes for POST method. One of the reasons is that by using GET method, the parameters or values passed within the form gets leaked or exposed in the link path. This opens up the chances that an attacker can steal information from the link path. If the values are a part of sensitive data, it would create a security issue. 

While on the other hand, POST is a secure way of handling any types of data (especially sensitive data). With POST, no values are exposed in the link path which alleviates the security risk.

Fix: 

## Flaw 4: Insufficient Logging & Monitoring
Description : While application may run properly meeting basic needs, it is a good practice to create log for monitoring the application. The depending on the type of log used, it helps the develop to keep track of any ongoing events or malicious activities. 

Fix: 

## Flaw 5: Broken Access Control
Description : 

