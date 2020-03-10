# Clue-Less

Ranbir Aulakh 
Parth Jalundhwala 
Michael Knatz 
Victoria Palaoro 

#### Setting up Dev Environment
1. Ensure you have Python 3.7 installed
2. Then execute `pip install requirements.txt` to install dependencies
3. Use any IDE

#### Start Client
Usage: python3 src/main.py [--type -t] <type>

ie:
    python3 src/main.py -t client

#### Start Server
WIP

##### Deploy Server Component(s) to Heroku
git add .
git commit -am "commit message"
git push heroku master
heroku run python src/server/server.py


##### Heroku disable web
heroku ps:scale web=0 

**CloueAMQP_URL** - Each URL supports up to 20 user connections (basically 5 games if there are 4 players in each game)
amqp://oczwxoia:Ed4t562v_dpmVP5P-j9EmwTBmz2Fc5RJ@termite.rmq.cloudamqp.com/oczwxoia
amqp://bdvzzyja:GqbzJa1YXO26se5uKe-_lS9jiSrNKQ63@termite.rmq.cloudamqp.com/bdvzzyja
