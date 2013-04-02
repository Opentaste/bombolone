# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~
    
    :copyright: (c) 2013 by Bombolone
""" 
# Imports outside Bombolone
import re
from datetime import datetime
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort 
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside Bombolone
import core.api.users
from core.users.users import User


def core_settings(user_id=None):
    """ """

    success = False
    message = ""

    if user_id:
        success = True
        message = ""
        user = core.api.users.find(user_id=user_id)
    
    data = {
        "success": success,
        "message": message,
        "user": user
    }

    return data