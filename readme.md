<img src="http://zizzamia.com/img/bombolone_logo.png"/>

### Bombolone version 0.3.2 ###

Bombolone is a tasty Content Management System for Python based on [Flask](http://flask.pocoo.org/), [MongoDB](http://www.mongodb.org/), [AngularJS](http://angularjs.org), [Sass](http://sass-lang.com) and [Bootstrap](http://getbootstrap.com/). 
It's designed to be a simple, flexible toolset for projects of any size.

## Some dependencies

- [Virtualenv](http://virtualenv.readthedocs.org/en/latest/)
- [MongoDB](http://www.mongodb.org/)
- [Fabric](http://www.fabfile.org/)
- [Rubygems](https://rubygems.org/)

## Quick start in 6 steps

```shell
# Run Mongodb
sudo mongod

# Clone the git repo in your new web app folder
git clone https://github.com/Opentaste/bombolone.git new_app

# Create your own environment from the new_app folder
cd new_app && virtualenv venv && . venv/bin/activate

# Install libries and init Bombolone Mongodb
fab install && fab init_database:name_database=new_app

# In a new tab with the same path run Compass
compass watch

# Run Bombolone 
python app.py
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

The core modules are as follows:
* Users
* Rank
* Pages
* Languages
* HashTable


## Core Modules

### Users ###
Allows user administration: 
* Administrators : can create, modify or delete users.
* Users : can only read the account list by default.

### Rank ###
The rank module allows you to see what ranks are available.

### Pages ###
Allows you to quickly create dynamic and static pages.
* Administrators : can create, edit, modify or delete pages.
* Users : can edit any content pages by default.

### Languages ###
From here you can decide which languages you want the site to use.

### HashTable ###
With the HashTable module you can create different hashmap be used inside modules or the site.
* Administrators : can create, edit, modify or delete hash map.
* Users : can edit any content of hash map by default.


## Tests
In Bombolone there is an environment for testing any module or webpage.

```
python unit_test.py 
```

## Who we are

Python and Javascript Lovers!

The project was created by [@zizzamia](https://twitter.com/Zizzamia). 

Contributors: [@jibbolo](https://twitter.com/jibbolo), [@proudlygeek](https://twitter.com/proudlygeek), [@diegor](https://twitter.com/diegor), [@danmaccauro](https://twitter.com/danmaccauro), [@bernarpa](https://twitter.com/bernarpa).

The logo was designed by [@FakeSamGregory](https://twitter.com/FakeSamGregory).


## License

* BSD
