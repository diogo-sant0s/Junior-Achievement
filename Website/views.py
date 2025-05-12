from flask import render_template, request, redirect, url_for
from main import app

@app.route('/')
def loaderpage():
    return render_template("loader.html")

@app.route('/info')
def infopage():
    return render_template("home.html")

@app.route('/contact')
def contactpage():
    return render_template("home.html")

@app.route('/home')
def homepage():
    return render_template("home.html")

@app.route('/UserDashboard')
def dashpage():
    return render_template("dashboard.html")