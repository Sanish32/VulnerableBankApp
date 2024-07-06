# Cyber Security Project 1

This is my project for Cyber Security Project for https://cybersecuritybase.mooc.fi/module-3.1. My project includes descriptions and fixes for each flow based on the OWASP Top Ten List of 2017.

My web application manages one or multiple bank accounts for users. It is a simple application that allows users to create an account, top up their balance, and display their existing accounts with their balances.

The project demonstrates five types of vulnerabilities, with comments providing fixes for each.

## Installation Instructions

1. Clone the directory
2. Run the server with: ``python3 manage.py runserver``
3. Go to ``http://localhost:8000/``

You can use the two premade users:

- ``username: alice``
``password: redqueen``

- ``username: bob``
``password: squarepants``

f you want to create a new user, open the terminal and navigate to this folder. Then, type ``python3 manage.py createsuperuser``. You will be prompted to enter a new username, email, and password. Enter the username and password, and skip the email section by pressing the Enter key. This will create a user with superuser status. 

To downgrade the status, you can choose one of the following methods:
i) type ``python3 manage.py shell``. 

``
from django.contrib.auth.models import User 
Update Bob's superuser status
bob = User.objects.get(username='bob')
bob.is_superuser = False
bob.save()
Update Alice's superuser status
alice = User.objects.get(username='alice')
alice.is_superuser = False
alice.save()
``

ii) Go to ``http://127.0.0.1:8000/admin/`` . Then, click on 'Users' under the 'AUTHENTICATION AND AUTHORIZATION' section. Next, click on the desired user and untick the 'staff' and 'superuser' status checkboxes.

## Flaw 1: Broken Authentication
Broken authentication occurs when an application lacks robust identification and authentication mechanisms. For instance, passwords that are guessable, short, or lack a combination of digits, lowercase, and uppercase letters are considered weak. To add on, users often use their username as their password to create an account quickly. These issues need to be addressed because attackers can easily crack weak passwords.

### Description: As of now, no password checks have been implemented, which is a significant vulnerability. 
Links: https://github.com/Sanish32/VulnerableBankApp/blob/e657c4fd108e1c9cbf70ab182a439057feff7fab/src/pages/views.py#L22

### Fixes: Password checking is implemented but currently commented out.
Links: https://github.com/Sanish32/VulnerableBankApp/blob/e657c4fd108e1c9cbf70ab182a439057feff7fab/src/pages/views.py#L26-L28

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

