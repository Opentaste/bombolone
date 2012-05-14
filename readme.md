<img src="http://zizzamia.com/img/bombolone_logo.png"/>

### Bombolone version 0.1.6 ###

Bombolone is a tasty Content Management System for Python based on [Flask](http://flask.pocoo.org/), [MongoDB](http://www.mongodb.org/), 
[Tiramisu](http://www.tiramisujs.com/) and [Twitter Bootstrap](http://twitter.github.com/bootstrap/). 
It's designed to be a simple, flexible toolset for projects of any size.



## Quick start

1. Clone the git repo `git clone git@github.com:OwlStudios/bombolone.git`

2. Move in Bombolone folder `cd bombolone/`

3. Install requirements  `pip install -r REQUIREMENTS.txt`

4. Move in app folder `cd app/`

5. Run Mongodb `mongod`

5. Restore last version Bombolone Mongodb `fab mongodb_restore`

6. Run Bombolone `python bombolone.py`

Registered users are:
* Admin with username 'admin' and password 'admin123'
* User with username 'user' and password 'user123'


## Overview

Sometimes you simply don’t need to use all the features of an entire CMS. 
Bombolone lets you have a good core, with five modules are essential 
for almost all web applications.

You can control them from the administration panel, and each has 
different tools to edit, create or delete.
It's important to note that beginning the application has two types 
of users: administrator and user classic. Administrator can do everything, 
but the User have only a limited set of tools to edit contents of other little things.

The core modules are as follows:
* Users
* Rank
* Pages
* Languages
* HashTable


## Core Modules

### Users ###
The User module allows administrators to create, modify and delete users.
The User module supports user rank, which can be set up permissions 
allowing each rank to do only what the administrator permits.
 
By default there are two users: Admin ( rank 10 ) and User ( rank  20 ).

### Rank ###
For now rank module only allows to see what rank they are available.

### Pages ###
Allows you to quickly create dynamic and static pages.

### Languages ###
From here you decide which languages you want to use the site.

### HashTable ###
With the HashTable module you can create different hashmap be used inside modules or the site.


## Who we are

Lovers of the python and the web!

The project was created by [Leonardo Zizzamia](http://zizzamia.com/). 

Contributors: Gianluca Bargelli, Giacomo Marinangeli, Paolo Bernardi, Rafael Lucas.

The logo was designed by Sam Gregory.


## License

* BSD
