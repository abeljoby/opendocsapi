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
                "_id": {"$oid": "unique-object-id"},
                "id": "document-id",
                "title": "Sample Document",
                "pages": [
                    {
                        "p_id": "page-1",
                        "heading": "Page 1 Heading",
                        "page_elements": [
                            {"Heading": {"id": "heading-1", "data": "Introduction", "htype": 1}},
                            {"Paragraph": {"id": "para-1", "data": "This is a paragraph."}},
                            {"Code": {"id": "code-1", "data": "print(\"Hello World\")", "lang": "python"}},
                            {"BulletList": {
                                "id": "list-1",
                                "lists": [
                                    {"id": "item-1", "value": "First item"},
                                    {"id": "item-2", "value": "Second item"}
                                ]
                            }},
                            {"Image": {"id": "image-1", "uri": "http://example.com/image.png"}}
                        ]
                    }
                ],
                "image_uri": "http://example.com/document-preview.png",
                "path": "/documents/doc1",
                "publish": True
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
