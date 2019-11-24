from flask import Flask, render_template, url_for, flash, redirect, session
#from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
from pdf2image import convert_from_path
# from dbconnect import connection
import mysql.connector
from werkzeug.utils import secure_filename
import re
import os

mcadisp = Flask(__name__, static_url_path='/static')
mcadisp.config['SECRET_KEY'] = 'fd5135666bac8fe98033e86b90251504'
UPLOAD_FOLDER = './static'
mcadisp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# mcadisp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(mcadisp)
mydb = mysql.connector.connect(
    host="localhost",
    user="aru",
    passwd="aru12345678",
    database="wireless"
)
mycursor = mydb.cursor(buffered=True)

@mcadisp.route("/display")
def display():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s """
        mycursor.execute(totaltime, (1, 1, 0, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('display.html', disp = disps, times = time[0])

if __name__ == '__main__':
    mcadisp.run(debug=True, port=5555)