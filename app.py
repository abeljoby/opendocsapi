from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from pydantic import BaseModel
from typing import List, Optional

class ListItem(BaseModel):
    id: str
    value: str

class PageElement(BaseModel):
    type: str  # Discriminator field to specify the element type
    id: str
    data: Optional[str] = None
    htype: Optional[int] = None
    lang: Optional[str] = None
    lists: Optional[List[ListItem]] = None
    uri: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "Paragraph",
                "id": "para-1",
                "data": "This is a paragraph."
            }
        }


class Page(BaseModel):
    p_id: str
    heading: str
    page_elements: List[PageElement]

class OID(BaseModel):
    oid: str

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
                "_id": {"oid": "unique-object-id"},
                "id": "document-id",
                "title": "Sample Document",
                "pages": [
                    {
                        "p_id": "page-1",
                        "heading": "Page 1 Heading",
                        "page_elements": [
                            {
                                "type": "Heading",
                                "id": "heading-1",
                                "data": "Introduction",
                                "htype": 1
                            },
                            {
                                "type": "Paragraph",
                                "id": "para-1",
                                "data": "This is a paragraph."
                            },
                            {
                                "type": "Code",
                                "id": "code-1",
                                "data": "print(\"Hello World\")",
                                "lang": "python"
                            },
                            {
                                "type": "BulletList",
                                "id": "list-1",
                                "lists": [
                                    {"id": "item-1", "value": "First item"},
                                    {"id": "item-2", "value": "Second item"}
                                ]
                            },
                            {
                                "type": "Image",
                                "id": "image-1",
                                "uri": "http://example.com/image.png"
                            }
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
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

chat_history = []

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
    try:
        completion = client.beta.chat.completions.parse(
            response_format=Document,
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a document generator platform. You will be given a topic and should generate a document in the given structure."
                },
                {"role": "user", "content": content}
            ]
        )
    except Exception as e:
        print(e)
        return jsonify(success=False, message=str(e)), 500

    try:
        response = completion.choices[0]
        text_content = response.message.parsed

        if text_content:
            # Convert the Document instance to a dictionary
            text_content_dict = text_content.model_dump()

            # Print the JSON response (for debugging purposes)
            print("JSON Response from OpenAI:", text_content_dict)  # You can also use logging

            # Append to chat history
            chat_history.append({"role": "assistant", "content": text_content_dict})

            return jsonify(success=True, message=text_content_dict)
        else:
            return jsonify(success=False, message="No text content found")
    except Exception as e:
        print(e)
        return jsonify(success=False, message=str(e)), 500

@app.route("/element", methods=["POST",])
def generate_element():
    content = request.json["message"]
    element_type = request.json["type"]
    print(content)
    message = f"Generate a {element_type} element about {content}."
    chat_history.append({"role":"user","content": content})
    try:
        completion = client.beta.chat.completions.parse(
            response_format=PageElement,
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a document generator platform. You will be given the type and topic of page element and should generate a page element in the given structure."
                },
                {
                    "role": "user",
                    "content": message,
                }
            ]
        )

    except Exception as e:
        print(e)
        return jsonify(success=False, message=str(e)), 500

    try:
        response = completion.choices[0]
        text_content = response.message.parsed

        if text_content:
            if element_type == "Image":
                image_prompt = completion.choices[0].message.parsed.data
                try:
                    image_completion = client.images.generate(
                        model="dall-e-3",
                        prompt=image_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_url = image_completion.data[0].url
                    text_content.uri = image_url
                    print(image_url)
                except Exception as e:
                    print(e)
                    return jsonify(success=False, message=str(e)), 500
            # Convert the Document instance to a dictionary
            text_content_dict = text_content.model_dump()

            # Print the JSON response (for debugging purposes)
            print("JSON Response from OpenAI:", text_content_dict)  # You can also use logging

            # Append to chat history
            chat_history.append({"role": "assistant", "content": text_content_dict})

            return jsonify(success=True, message=text_content_dict)
        else:
            return jsonify(success=False, message="No text content found")
    except Exception as e:
        print(e)
        return jsonify(success=False, message=str(e)), 500