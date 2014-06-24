# -*- coding: utf-8 -*-
"""
web_pages.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
from flask import request, session, g

# Imports inside Bombolone
from decorators import get_template
from core.utils import get_content_dict

@get_template("pages")
def contact(page, url, code):
    """ """
    title       = page['title'][code]
    description = page['description'][code]
    content     = get_content_dict(page, code)
    
    if request.method == 'POST':
        text = request.form['text']
        name = request.form['name']
        email = 'name@domain.com'
        title = 'Info'
        text_email = """\
        <h3>I'm """+name+"""</h3>
        <p style="font-size:15px">"""+text+"""</p>"""
        text = 'I\'m %s \n %s' % (name, text)
        send_email(title, text, text_email, email)
        g.message = 'email sent'
        g.status = 'mes-green'