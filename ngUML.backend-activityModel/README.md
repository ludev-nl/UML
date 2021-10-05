# DemoUML

Ralph's project -> `./firstExample/model`  
Tiantian -> `./firstExample/extractor`  

Install all the packages using `pip install -r requirement.txt`

Copy the settings.example.py file and rename to settings.py
Add the following line to settings.py at the secret key comment.
```
SECRET_KEY = 'SECRET_KEY'
```
A secret key can be generated with https://djecrety.ir/ , replace 'SECRET_KEY' with the generated key.

To start the server use: ```python3 manage.py runserver```
