from flask import Flask, Blueprint, request, jsonify, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
import os, requests, json

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
@site.route("/books")
def index():
    if session.get("logged_in") is None:
        return redirect("/login")
    if session.get("logged_in") == False:
        return redirect("/login")
    response = requests.get("http://127.0.0.1:5000/api/books")
    data = json.loads(response.text)

    return render_template("index.html", books = data)

@site.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        if (request.form['username'] == "username") and (request.form['password'] == "password"):
            session['logged_in'] = True
            return redirect("/")
    return render_template("login.html")

@site.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/login")

@site.route("/add", methods = ["GET", "POST"])
def add():
    if session.get("logged_in") is None:
        return redirect("/login")
    if session.get("logged_in") == False:
        return redirect("/login")
    if(request.method == "GET"):
        return render_template("add.html")
    
    Title = request.form.get("Title")
    Author = request.form.get("Author")
    PublishedDate = request.form.get("PublishedDate")
    
    data = {
        "Title": Title,
        "Author": Author,
        "PublishedDate": PublishedDate
    }
    headers = {
        "Content-type": "application/json"
    }
    
    requests.post("http://127.0.0.1:5000/api/add", data = json.dumps(data), headers = headers)
    
    return redirect("/")

@site.route("/update", methods = ["GET", "POST"])
def bookUpdate():
    if session.get("logged_in") is None:
        return redirect("/login")
    if session.get("logged_in") == False:
        return redirect("/login")
    if(request.method == "GET"):
        return render_template("update.html")
    
    BookID = request.form.get("BookID")
    Title = request.form.get("Title")
    Author = request.form.get("Author")
    PublishedDate = request.form.get("PublishedDate")
    
    data = {
        "BookID": BookID,
        "Title": Title,
        "Author": Author,
        "PublishedDate": PublishedDate
    }
    headers = {
        "Content-type": "application/json"
    }
    
    requests.post("http://127.0.0.1:5000/api/update",
                  data = json.dumps(data), headers = headers)
    
    return redirect("/books")

@site.route("/delete", methods = ["GET", "POST"])
def deleteBook():
    if session.get("logged_in") is None:
        return redirect("/login")
    if session.get("logged_in") == False:
        return redirect("/login")
    if(request.method == "GET"):
        return render_template("delete.html")
    
    BookID = request.form.get("BookID")
    
    data = {
        "BookID": BookID,
    }
    headers = {
        "Content-type": "application/json"
    }
    
    requests.post("http://127.0.0.1:5000/api/delete",
                  data = json.dumps(data), headers = headers)
    
    return redirect("/books")

@site.route("/report")
def generateReport():
    return render_template("report.html")