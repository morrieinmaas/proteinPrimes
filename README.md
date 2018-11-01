## Swiss Army knife prime factoring

Welcome to another demo project that evolves around prime factoring. 

### Overview

_What does it do?_ Quite simple. The project, when running, calculates prime factors of integers. You can go to _localhost:8000_ and watch
jobs for random numbers being spawned and submitted and you may as well submit your own number you want to know the prime factors of. 
You can see the latest 10 jobs and they instantly show up when submitted and you will instantly receive a notification when a job completes.

_Sounds simple(ish) - how does it work?_ A little more complex. I tried to combine a few bits and bobs I hadn't combined or even used before really.
The main server is a Django instance. It serves you with and handles your interaction with the UI. This happens via models (remember the MVC framwork?!). 
That means data gets handled via models, but is ultimately residing in a database. In order to not use SQLite and to try something new (partially motivated by JSONField()) 
I decided to give PostgreSQL a go. In combination with Django and Docker, at least for this simple case, pretty straight forward compared to other production-ready DBs.
Speaking of which - there is another DB instance running with this project. It's REDIS, the RAM-based DB, that acts as a broker for the tasks we are running.

So who is running them? If you take a look at the docker-compose.yaml you will find a celery instance. Celery is our designated work horse running the tasks.

_And how does it all come together?_ There is two parts to that. First of all, the project uses websockets/django channels(1) to communicate tasks between the instances. Thsi has
the advantage that we can spawn many tasks via the Django server and submit them. Redis will handle (handy in case there more celery workers) distributing them to the workers, where tasks get queued. 
Sockets make the long-poling obsolete so you instantly get the result when it's send a sopposed to GET/POST back and forth. We also create and update the tasks via 
the models to our PostgreSQL instance, so nothing gets lost.
The second part is running everything containerized. Docker Swarm has some great feature - for example, it uses secure communication within the swarm by default. This is done
issueing CA certificates for all containers in the swarm. You can also specify custom certificates from the CLI. This saves a whole lot of time securing sucha setup part by part. 
In order to make it a bit easier on resources and save people the trouble of creating a docker registry in their local environment, the projects uses a docker overlay network
with encryption, which you can also find specified in the docker-compose.yaml. This is pretty much a shortcut to creating a single node swarm on your local machine. 

So why have I done it this way? As said, it handles some simple scenario and yet incorporates a variety of (at least to me) interesting technologies and a (not quite perfect) way 
to bunde them together into something that works. 

I hope you enjoy it, find it useful and you're most welcome to suggest improvements.

### Installation

I've tested the setup on Linux, but this should work for any UNIX system with a bash shell.

* _Prerequisits:_ Make sure you have docker and docker-compose (and git) installed and avaiable in your $PATH. Also, make sure docker deamon is actually enbaled and running.
  * It's also a good idea to check what containers are currently running and what ports they use to avoid conflicts (this project wil occupy 8000, 6379 and 5432).
  * Check whether you have added something like `127.0.0.1   localhost` added to your /etc/hosts to make the composed containers available on your localhost
* Clone the repo with `git clone https://github.com/morrieinmaas/proteinPrimes`
* Change into the project folder `cd proteinPrimes`
* Simply run it with `bash start_it.sh` - this will use the Dockerfile, docker-compose.yaml with a terminal commands to let you sit back and relax
  * You will be prompted to create a user and password which is for the django admin backend
  * Comment out the respective command in the bash script if you have created a user already and/or do not want to create another one

And that should be it. You can navigate to the app in your browser on _localhost:8000_ and go to the django admin view by adding a _/admin_ to that.

### Possible improvements

* improve templating using base.html etc.
* move javascript from index.html to separate file. It's now parked where it is to make it easier to follow what going on.
* Replace the JS random job generation by a cron/periodic job for instance with celery\_beat\_schedule
* Inspite of the previous point, we can also achieve this switching to django channels2 in the consumers.py. Channels2 works quite differently to Channels1.
* Use proper Django forms for submissions and validation

### TODOs

This project still needs testing. I'll add that as soon as possible.
