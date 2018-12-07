# Tipsyapp

This angular 5 web app parses recipes from the "Tispy Bartender" and allows users to input ingredients they have at home to see which of his drinks they can make.

## Installation
1. `mkdir tipsyapp`  
2. `cd tipsyapp`  
3. `git clone https://github.com/nelsondude/tipsyapp_backend.git`  
4. `git clone https://github.com/nelsondude/tipsyapp_client.git`  
5. `cd tipsyapp_client  && npm install`  
6. `ng build --prod --output-path ../tipsyapp_backend/tipsyapp/static/ang/ --output-hashing none`  
7. `cd ../tipsyapp_backend`  
8. `python3 install pipenv`  
9. `pipenv shell`  
10. `pip install -r requirements.txt`  
11. `python manage.py runserver`

## Deployment
1. `ng build --prod --output-path ../tipsyapp_backend/tipsyapp/static/ang/ --output-hashing none`
2. `cd ../tipsyapp_backend`
3. `git add . && git commit -m "Message here"`
4. `git push origin master`  - master push triggers heroku build