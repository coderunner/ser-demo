from dataclasses import dataclass
import xml.etree.ElementTree as ET
import json

@dataclass
class Book:
    id: str
    title: str
    author: str

def to_dict(book): 
    return book.__dict__

def book_to_xml_element(book): 
    b = ET.Element('Book')
    ET.SubElement(b, 'Id').text = book.id
    ET.SubElement(b, 'Title').text = book.title
    ET.SubElement(b, 'Author').text = book.author
    return b

def books_to_xml_element(books):
    b = ET.Element('Books')
    for book in books :
      b.append(book_to_xml_element(book))
    return b

def from_json_data(data): 
    d = json.loads(data)
    return Book(None, d['title'],d['author'])

def from_xml_data(data):
    book = ET.fromstring(data)
    return Book(None, book.find('Title').text,book.find('Author').text)