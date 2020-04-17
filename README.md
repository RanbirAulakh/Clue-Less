# Clue-Less

Ranbir Aulakh 
Parth Jalundhwala 
Michael Knatz 
Victoria Palaoro 

#### Setting up Dev Environment
1. Ensure you have Python 3.7 installed
2. Then execute `pip install requirements.txt` to install dependencies
3. Use any IDE

#### Start Django Server
`cd ClueLess/`

If this is an initial setup or if you have made some changes to the Model classes, run the commands below:

- `python3 manage.py makemigrations`

- `python3 manage.py migrate`

`python3 manage.py runserver`

Then open web broswer (Chrome, Firefox, or Edge) and go to `http://127.0.0.1:8000/`

**What is ___?**
- Procfile
    - It's a file that runs python in the background on Heroku
- runtime.txt
    - Let Heroku know which Python version to use
- requirements.txt
    - Travis-CI or Heroku can download required dependencies in order to run the game
    - django - Python web framework
    - channels - Message communication
    - django-redis - Message communication (data store)


#### (WIP) Deploy Django to Heroku
git add .
git commit -am "commit message"
git push heroku master

