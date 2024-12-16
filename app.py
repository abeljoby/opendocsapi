from flask import Flask, flash, render_template, request, jsonify
from openai import OpenAI
import os

from pydantic import BaseModel,RootModel
from typing import List, Union

class OID(BaseModel):
    oid: str

class ID(BaseModel):
    id: str

class HeadingElement(BaseModel):
    id: str
    data: str
    htype: int

class ParagraphElement(BaseModel):
    id: str
    data: str

class CodeElement(BaseModel):
    id: str
    data: str
    lang: str

class ListItem(BaseModel):
    id: str
    value: str

class BulletListElement(BaseModel):
    id: str
    lists: List[ListItem]

class ImageElement(BaseModel):
    id: str
    uri: str

class PageElement(RootModel):
    root : Union[
        HeadingElement,
        ParagraphElement,
        CodeElement,
        BulletListElement,
        ImageElement
    ]

class Page(BaseModel):
    p_id: str
    heading: str
    page_elements: List[PageElement]

class Document(BaseModel):
    _id: OID
    id: str
    title: str
    pages: List[Page]
    image_uri: str
    path: str
    publish: bool

    class Config:
        json_schema_extra = {
            "example": {
                "_id": {"$oid": "66ab314b67082310f8c1dc4a"},
                "id": "369",
                "title": "Sample Document",
                "pages": [
                    {
                        "p_id": "668014e8ad94a2476284f09d",
                        "heading": "Page 1 Heading",
                        "page_elements": [
                            {"Heading": {"id": "66a27f0cd819929a916e742b", "data": "Introduction", "htype": 1}},
                            {"Paragraph": {"id": "66a53f95ccb9935788357c85", "data": "This is a paragraph."}},
                            {"Code": {"id": "67234b8b72dca6c708d134c6", "data": "print(\"Hello World\")", "lang": "python"}},
                            {"BulletList": {
                                "id": "list-1",
                                "lists": [
                                    {"id": "66923fe319bc07581ce3647b", "value": "First item"},
                                    {"id": "66bcbb5903ac6c52820e3d8a", "value": "Second item"}
                                ]
                            }},
                            {"Image": {"id": "66cb593378a693fe12d2792d", "uri": "http://example.com/image.png"}}
                        ]
                    }
                ],
                "image_uri": "http://example.com/document-preview.png",
                "path": "/documents/doc1",
                "publish": "true"
            }
        }

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

app = Flask(__name__)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

@app.route("/", methods=['GET','POST'])
@app.route("/<name>", methods=['GET','POST'])
def index(name=None):
    return render_template("index.html",person=name, chat_history=chat_history)

@app.route("/prompt", methods=["POST"])
def send_prompt():
    content = request.json["message"]
    chat_history.append({"role":"user","content": content})
    completion = client.chat.completions.create(
    response_format="json",
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ]
    )

    text_content = None
    response = completion.choices[0]
    text_content = response.message.content
    if text_content:
        chat_history.append({"role":"assistant","content":text_content})
        return jsonify(success=True,message=text_content)
    else:
        return jsonify(success=False,message="No text content found")

@app.route("/document", methods=["POST"])
def generate_document():
    content = request.json["message"]
    chat_history.append({"role":"user","content": content})
    completion = client.beta.chat.completions.parse(
        response_format=Document,
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a document generator platform. You will be given a topic and should convert it into the given structure."},
            {"role": "user", "content": content}
        ]
    )

    text_content = None
    response = completion.choices[0]
    text_content = response.message.parsed
    if text_content:
        chat_history.append({"role":"assistant","content":text_content})
        return jsonify(success=True,message=text_content)
    else:
        return jsonify(success=False,message="No text content found")
