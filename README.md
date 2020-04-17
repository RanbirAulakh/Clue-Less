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

`python3 manage.py makemigrations (one time)`

`python3 manage.py migrate (one time)`

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


#### (WIP) Deploy Django to Heroku (For Production Only)
git add .
git commit -am "commit message"
git push heroku master

##### Heroku disable web
heroku ps:scale web=0 

**CloueAMQP_URL** - Each URL supports up to 20 user connections (basically 5 games if there are 4 players in each game)
amqp://oczwxoia:Ed4t562v_dpmVP5P-j9EmwTBmz2Fc5RJ@termite.rmq.cloudamqp.com/oczwxoia
amqp://bdvzzyja:GqbzJa1YXO26se5uKe-_lS9jiSrNKQ63@termite.rmq.cloudamqp.com/bdvzzyja

**LocalHost URL**
amqp://guest:guest@localhost:5672/%2f


##### Create Installer (For Production Only)
WIP

