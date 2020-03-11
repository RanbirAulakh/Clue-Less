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

#### Start Server on Localhost

##### Mac OS Setup
`brew update`

`brew install rabbitmq` to install rabbitmq

`export PATH=$PATH:/usr/local/opt/rabbitmq/sbin` 

`rabbitmq-server` to start the server

Server should be up and running. Then execute

`python3 src/main.py -t server`

##### Windows 

#### Deploy Server Component(s) to Heroku (For Production Only!)
git add .
git commit -am "commit message"
git push heroku master
heroku run python src/server/server.py


##### Heroku disable web
heroku ps:scale web=0 

**CloueAMQP_URL** - Each URL supports up to 20 user connections (basically 5 games if there are 4 players in each game)
amqp://oczwxoia:Ed4t562v_dpmVP5P-j9EmwTBmz2Fc5RJ@termite.rmq.cloudamqp.com/oczwxoia
amqp://bdvzzyja:GqbzJa1YXO26se5uKe-_lS9jiSrNKQ63@termite.rmq.cloudamqp.com/bdvzzyja

**LocalHost URL**
amqp://guest:guest@localhost:5672/%2f


**What is ___?**
- Procfile
    - It's a file that runs python in the background on Heroku
- runtime.txt
    - Let Heroku know which Python version to use
- requirements.txt
    - Travis-CI or Heroku can download required dependencies in order to run the game
    - pygame - 2D Game Engine
    - pika - RabbitMQ Messages Notification
    - inquirer - Prompt User with options
    - aioamqp - Multithreading Messages
