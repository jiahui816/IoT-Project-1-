from flask import Flask, Blueprint, request, jsonify, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text)
    Author = db.Column(db.Text)
    PublishedDate = db.Column(db.Date)
    

    def __init__(self, BookID, Title, Author, PublishedDate):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PublishedDate")

bookSchema = BookSchema()
booksSchema = BookSchema(many = True)

@api.route("/api/books", methods = ["GET"])
def getBooks():
    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)

@api.route("/api/add", methods = ["POST"])
def addBook():
    Title = request.json["Title"]
    Author = request.json["Author"]
    PublishedDate = request.json["PublishedDate"]
   
    book = Book(None,Title,Author,PublishedDate)  
    db.session.add(book)
    db.session.commit()
    
    return bookSchema.jsonify(book)

@api.route("/api/update", methods = ["POST"])
def bookUpdate():
    BookID = request.json["BookID"]
    newTitle = request.json["Title"]
    newAuthor = request.json["Author"]
    newPublishedDate = request.json["PublishedDate"]
    
    book = Book.query.get(BookID)
    book.Title = newTitle
    book.Author = newAuthor
    book.PublishedDate = newPublishedDate
    
    db.session.commit()
    
    return bookSchema.jsonify(book)

@api.route("/api/delete", methods = ["POST"])
def bookDelete():
    BookID = request.json["BookID"]
    book = Book.query.get(BookID)
    db.session.delete(book)
    db.session.commit()
    return bookSchema.jsonify(book)