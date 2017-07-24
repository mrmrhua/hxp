from flask import render_template,request,session,redirect,url_for
from . import add_project

@add_project.route('/admin/pm')
def addproject():
    return  render_template('admin/addpro.html')

