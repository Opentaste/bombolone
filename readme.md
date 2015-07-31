<img src="http://zizzamia.com/img/bombolone_logo.png"/>

### Bombolone version 0.3.3 ###

Bombolone is a tasty Content Management System for Python based on [Flask](http://flask.pocoo.org/), [MongoDB](http://www.mongodb.org/), [AngularJS](http://angularjs.org), [Sass](http://sass-lang.com) and [Bootstrap](http://getbootstrap.com/). 
It's designed to be a simple, flexible toolset for projects of any size.

Based from the Python and Angular implementation of [Opentaste.co](http://opentaste.co/).


## Important dependecies
Before starting check if you have all you need.
```shell
# Install Homebrew
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

# Install MongoDB
brew install mongodb

# Install Virtualenv
sudo pip install virtualenv
```
Important, if you use a Mac OSX please install the commandline tools 
manually from Apple's Developer site.
[developer.apple.com/downloads/…](https://developer.apple.com/downloads/index.action?=command%20line%20tools#)

## Quick start
Just for running a new app let's follow these 6 steps.
```shell
# Clone the latest stable version in your new web app folder
git clone --branch 0.3.3 https://github.com/Opentaste/bombolone.git new_app && cd new_app

# Run Mongodb
sudo mongod

# Create your own environment from the new_app folder
virtualenv venv && . venv/bin/activate

# Install libraries
python setup.py install && cd bombolone

# Init Bombolone Mongodb
bombolone bake

# Run Bombolone 
bombolone serve
```

Registered users are:
* Admin with username 'admin' and password 'admin123'
* User with username 'user' and password 'user123'


## Overview

Sometimes you simply don’t need to use all the features of a CMS. 
Bombolone lets you have a good core, with five modules are essential 
for almost all web applications.

You can control them from the administration panel, and each has 
different tools to edit, create or delete.
It's important to note that beginning the application has two types 
of users: administrators and users. Administrator can do everything. 
Users can only edit content and other little things,
but configurable to allow multiple levels of access depending on rank.


## Core Modules

#### Users ####
Allows user administration: 
* Administrators : can create, modify or delete users.
* Users : can only read the account list by default.

#### Rank ####
The rank module allows you to see what ranks are available.

#### Pages ####
Allows you to quickly create dynamic and static pages.
* Administrators : can create, edit, modify or delete pages.
* Users : can edit any content pages by default.

#### Languages ####
From here you can decide which languages you want the site to use.

#### HashTable ####
With the HashTable module you can create different hashmap be used inside modules or the site.
* Administrators : can create, edit, modify or delete hash map.
* Users : can edit any content of hash map by default.


## How compile CSS
Setting up the ruby environment
```shell
gem update --system
gem install compass
gem install compass-h5bp
```

In a new tab with the same path run [Compass](http://compass-style.org/)
```shell
compass watch
```


## Fabric command-line
We use [Fabric](http://www.fabfile.org/) to provide a basic suite of operations for executing local 
or remote shell commands, as well as auxiliary functionality such as prompting the 
running user for input, or aborting execution.
If you find trouble to installing Fabric, you can check this [page](http://www.fabfile.org/installing.html).

```shell
pip install fabric
sudo pip install yuicompressor
```

Available commands:

Check if is running the MongoDB database
```shell
fab check_database
```

Init the basic database
```shell
fab init_database            
```

```shell
fab local_backup
```

Minify .js files that have been changed since last run
```shell
fab minify                   
```

```shell
fab mongodb_restore
```

```shell
fab update
```

```shell
fab write_db_in_config
```


## Tests

#### Python ####
Run python test
```shell
python unit_test.py 
```

#### Js Unit/Integration Tests ####
Before run the test, you need install some dependecies.
Download and install Node from [http://nodejs.org/download/](http://nodejs.org/download/)
If you never use Protractor before you can have a quick intro [here](http://ramonvictor.github.io/protractor/slides/#/).
```shell
# Install Nvm
curl https://raw.githubusercontent.com/creationix/nvm/v0.11.1/install.sh | bash

# Select Nvm
nvm alias default v0.10.29

# Installing all node packaged modules
npm install

# Install Protractor global
npm install -g protractor

# Install Selenium
webdriver-manager update
```

Run Unit tests
```shell
npm test
```

Run Integration tests not log in
```shell
webdriver-manager start
protractor conf.js
```

Run Integration tests as admin
```shell
webdriver-manager start
protractor conf.js --params.admin true --params.login.user 'admin' --params.login.password 'admin123'
```

## Who we are

Python and Javascript Lovers!

The project was created by [@zizzamia](https://twitter.com/Zizzamia). 

Contributors: [@jibbolo](https://twitter.com/jibbolo), [@proudlygeek](https://twitter.com/proudlygeek), [@diegor](https://twitter.com/diegor), [@danmaccauro](https://twitter.com/danmaccauro), [@bernarpa](https://twitter.com/bernarpa).

The logo was designed by [@FakeSamGregory](https://twitter.com/FakeSamGregory).


## License

* BSD
