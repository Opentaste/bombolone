<img src="http://zizzamia.com/img/bombolone_logo.png"/>

### Bombolone version 0.1.6 ###

Bombolone is a tasty Content Management System for Python based on [Flask](http://flask.pocoo.org/), [MongoDB](http://www.mongodb.org/), 
[AngularJS](http://angularjs.org), [jQuery](http://jquery.com), [Sass](http://sass-lang.com) and [Twitter Bootstrap](http://twitter.github.com/bootstrap/). 
It's designed to be a simple, flexible toolset for projects of any size.



## Quick start

1. Clone the git repo `git clone git@github.com:OwlStudios/bombolone.git`

2. Move in Bombolone folder `cd bombolone/`

3. Install requirements  `pip install -r REQUIREMENTS.txt`

4. `gem install compass`

5. Move in app folder `cd app/`

6. Run Mongodb `mongod`

7. Restore last version Bombolone Mongodb `fab mongodb_restore`

8. Run Compass `compass watch`

8. Run Bombolone `python bombolone.py`

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


## Who we are

Lovers of the python and the web!

The project was created by [Leonardo Zizzamia](http://zizzamia.com/). 

Contributors: Gianluca Bargelli, Giacomo Marinangeli, Paolo Bernardi, Rafael Lucas, Michael Cable.

The logo was designed by Sam Gregory.


## License

* BSD
