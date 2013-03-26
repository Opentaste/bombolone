# -*- coding: utf-8 -*-
"""
    web_pages.py
    ~~~~~~
    
    :copyright: (c) 2012 by Leonardo Zizzamia
    :license: BSD (See LICENSE for details)
""" 
# Imports outside bombolone
from flask import request, session, g, render_template, url_for, redirect

def contact(page, url, code):
    """ """
    title       = page['title'][code]
    description = page['description'][code]
    content     = page['content'][code]
    
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
    
    return render_template('pages/'+page['file']+'.html', **locals())