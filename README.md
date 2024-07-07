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

To downgrade the status, you can choose one of the following methods:<br />
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

### Vulnerable: As of now, no password checks have been implemented, which is a significant vulnerability. 
Link: https://github.com/Sanish32/VulnerableBankApp/blob/e657c4fd108e1c9cbf70ab182a439057feff7fab/src/pages/views.py#L22

### Fix: Password checking is implemented but currently commented out.
Links: 
https://github.com/Sanish32/VulnerableBankApp/blob/e657c4fd108e1c9cbf70ab182a439057feff7fab/src/pages/views.py#L26-L28
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L35-L36

## Flaw 2: SQL Injection
Another vulnerability is SQL injection, where an attacker can manipulate a SQL query by injecting malicious SQL code into the web application. In my application, if an attacker manages to manipulate a SQL query and inserts their IBAN, they could receive money instead of the intended user who is topping up their account.

To mitigate this issue, avoid using traditional SQL queries directly. Instead, leverage Django's ORM (Object-Relational Mapping) or use parameterized queries, which help prevent SQL injection vulnerabilities.

### Vulnerable: As of now, when the user tops up the money, the balance is updated in the database using a traditional SQL query.
Link: 
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L101-L104
https://github.com/Sanish32/VulnerableBankApp/blob/ac23f8c9181638c1583beb6298afebf4e755dffd/src/pages/views.py#L137-L138

### Fix: The solution is to use Django's ORM instead of raw SQL for updating the balance.
Link: https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L128-L131

## Flaw 3: Sensitive Data Exposure
In HTML forms, there are primarily two methods for sending data to the server: GET and POST. Both can serve the same purpose, but there are key differences between them.

The GET method should be used when the form does not include any sensitive data. In contrast, the POST method is recommended for forms containing sensitive data. One reason for this distinction is that with the GET method, the parameters or values passed within the form are exposed in the URL query string. This exposes them to potential interception by attackers, posing a security risk, especially if the values include sensitive information.

On the other hand, the POST method provides a more secure way of handling any type of data, particularly sensitive data. With POST, the values are not exposed in the URL, which mitigates the security risk associated with data interception through the link path.

### Vulnerable: Since the GET method is used to send the form, parameters from the form are exposed in the URL.
Links: 
https://github.com/Sanish32/VulnerableBankApp/blob/93a057ffcf57450390a578de58a9518cea6ce38b/src/pages/templates/pages/index.html#L70-L80
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L21-L22
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L83-L85

### Fixes: When an account is created, the form is sent via the POST method. Additionally, the user is redirected to the home page after account creation.
Links: 
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L87-L88
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L14-L19

## Flaw 4: Insufficient Logging & Monitoring
While the application may function properly meeting basic needs, it is considered good practice to implement logging for monitoring the application. Depending on the type of logging implemented, it helps developers track ongoing events and detect malicious activities.

### Fix: Different logging events are enabled
Links: 
https://github.com/Sanish32/VulnerableBankApp/blob/830c2c695c32305b810c65d085995c3f4a04d100/src/pages/views.py#L8-L9
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L30-L31
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L38-L39
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L47-L48
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L56-L57
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L63-L64
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L72-L73
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L80-L81
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L119-L120
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L152-L153
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L160-L161
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L168-L169
https://github.com/Sanish32/VulnerableBankApp/blob/b8da51c5b0b5a46344142ef6921bc3c5cc90a87c/src/pages/views.py#L177-L178

## Flaw 5: Broken Access Control
When an application fails to restrict unintended actions by users, it exhibits broken access control. For example, when deleting an account, if a user accidentally enters the wrong IBAN, they could lose access to their account.

Similarly, in the case of topping up money, if a user mistakenly enters a wrong IBAN, the money could be transferred to the incorrect account.

To prevent these scenarios, it's crucial to verify that actions such as topping up money or deleting an account are performed only on accounts belonging to the logged-in user.

### Vulnerable: Account is retrieved based on iban number.
Links:
https://github.com/Sanish32/VulnerableBankApp/blob/93bf24c2e82ad3344492c9c9644b18b688e3e908/src/pages/views.py#L148-L149
https://github.com/Sanish32/VulnerableBankApp/blob/93bf24c2e82ad3344492c9c9644b18b688e3e908/src/pages/views.py#L110-L111

### Fix: Account is retrieved based on iban number which belongs to the logged in user. To avoid this issue, we can show the list of accounts that belongs to the user as an option. This way, the user does not have to manually type in the IBAN.
Links:
https://github.com/Sanish32/VulnerableBankApp/blob/93bf24c2e82ad3344492c9c9644b18b688e3e908/src/pages/views.py#L113-L117
https://github.com/Sanish32/VulnerableBankApp/blob/93bf24c2e82ad3344492c9c9644b18b688e3e908/src/pages/views.py#L150-L151
https://github.com/Sanish32/VulnerableBankApp/blob/d526ff02964690e2fc7f0947e994a01873e81d3b/src/pages/templates/pages/index.html#L35-L53
https://github.com/Sanish32/VulnerableBankApp/blob/d526ff02964690e2fc7f0947e994a01873e81d3b/src/pages/templates/pages/index.html#L55-L68
