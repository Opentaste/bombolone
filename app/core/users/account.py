# -*- coding: utf-8 -*-
"""
    account.py
    ~~~~~~
    
    :copyright: (c) 2012 by Opentaste
""" 
# Imports outside Opentaste
import re
from datetime import datetime
from flask import Blueprint, request, session, g, Response, render_template, url_for, redirect, abort 
from pymongo import ASCENDING, DESCENDING
from pymongo.objectid import ObjectId

# Imports inside opentaste
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