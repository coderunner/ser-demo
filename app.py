from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from book import *
from werkzeug.exceptions import UnsupportedMediaType

import xml.etree.ElementTree as ET
import uuid

app = Flask('SER_DEMO')

BOOKS = [Book(str(uuid.uuid4()), 'Le bon livre', 'H. Lebon'), Book(str(uuid.uuid4()),'Un autre bon livre', "B. LeBonAussi")]

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_XML = "application/xml"

@app.route("/books")
def get_books():
    content_type = request.headers.get('accept')

    if CONTENT_TYPE_JSON in content_type:
      json = jsonify(list(map(to_dict, BOOKS)))
      response = make_response(json)
      response.content_type = CONTENT_TYPE_JSON
      return response

    elif CONTENT_TYPE_XML in content_type:
      element = books_to_xml_element(BOOKS)
      xml = ET.tostring(element, encoding='utf8', method='xml')
      response = make_response(xml)
      response.content_type = CONTENT_TYPE_XML
      return response
    
    else:
      raise UnsupportedMediaType()

@app.route("/books", methods=["POST"])
def post_book():
    content_type = request.headers.get('content-type')
    data = request.get_data()

    if CONTENT_TYPE_JSON in content_type:
      new_book_data = from_json_data(data)
      new_book = create_new_book(new_book_data)
      BOOKS.append(new_book)

      json = jsonify(to_dict(new_book))
      response = make_response(json)
      response.content_type = CONTENT_TYPE_JSON
      return response
    elif CONTENT_TYPE_XML in content_type:
      new_book_data = from_xml_data(data)
      new_book = create_new_book(new_book_data)
      BOOKS.append(new_book)

      xml = ET.tostring(book_to_xml_element(new_book), encoding='utf8', method='xml')
      response = make_response(xml)
      response.content_type = CONTENT_TYPE_XML
      return response
    
    else:
      raise UnsupportedMediaType()

def create_new_book(book_data):
    id = str(uuid.uuid4())
    return Book(id, book_data.title, book_data.author)
    
    
