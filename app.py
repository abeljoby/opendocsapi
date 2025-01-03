from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import hashlib
import time
from pydantic import BaseModel
from typing import List, Union

class HeadingElement(BaseModel):
    id: str
    data: str
    htype: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": "66ad15df3e2b4e1de23b3af5",
                "data": "Building Backend",
                "htype": 1
            }
        }

class HeadingObject(BaseModel):
    Heading: HeadingElement

class ParagraphElement(BaseModel):
    id: str
    data: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "66ad16093e2b4e1de23b3af7",
                "data": "Actix-web is a framework in rust to build complex highly sclable and blazingly fast web backends,it include features like logging chaining,middlewares,loggers,sharing database pool for multiple databses etc.\n\nwe will dive deep into building complex parts of backend,so that you can start building your idea."
            }
        }

class ParagraphObject(BaseModel):
    Paragraph: ParagraphElement

class CodeElement(BaseModel):
    id: str
    data: str
    lang: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "66bf7aee545b521aeaebb02f",
                "data": "pub async fn get_courses()->impl Responder{\n     match get_user_repository().await{\n          Ok()=>{\n               return HttpResponse::Ok()\n          },\n          Err()=>{\n               return HttpResponse::BadRequest()\n          }\n     }\n}",
                "lang": "rust"
            }
        }

class CodeObject(BaseModel):
    Code: CodeElement

class ListItem(BaseModel):
    id: str
    value: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "66bcbb5903ac6c52820e3d8a",
                "value": "One of the standout features of Rust is its ownership system, which ensures memory safety without needing a garbage collector."
            }
        }

class BulletListElement(BaseModel):
    id: str
    lists: List[ListItem]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "669179ba693714ddce85cd83",
                "lists": [
                {
                    "id": "66923fe319bc07581ce3647b",
                    "value": "Rust is a systems programming language that has gained significant attention and popularity since its inception.                                                            "
                },
                {
                    "id": "66bcbb5903ac6c52820e3d8a",
                    "value": "One of the standout features of Rust is its ownership system, which ensures memory safety without needing a garbage collector."
                },
                {
                    "id": "669179d8693714ddce85cd85",
                    "value": "Its primary design goals are safety, speed, and concurrency. Rust is syntactically similar to C++ but provides better memory safety while maintaining performance."
                },
                {
                    "id": "66917a00693714ddce85cd87",
                    "value": "This system enforces strict rules on how memory is managed, significantly reducing the likelihood of null pointer dereferences, buffer overflows, and data races."
                },
                {
                    "id": "66bcbb6103ac6c52820e3d8b",
                    "value": "Become super proficient in Rust to get job in companies like Anthropic,Microsoft,Openai,and Ola cabs."
                },
                {
                    "id": "67147fbdbece8b4af9fa2bf7",
                    "value": "Hai everyone this is bullet line number six..."
                }
                ]
            }
        }

class BulletListObject(BaseModel):
    BulletList: BulletListElement

class ImageElement(BaseModel):
    id: str
    uri: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "66cb593378a693fe12d2792d",
                "uri": "https://cdn.torchend.com/meta_c2b83f09f7f764cd902a3ba3"
            }
        }

class ImageObject(BaseModel):
    Image: ImageElement

class PageElements(BaseModel):
    list: List[Union[ParagraphObject, HeadingObject, CodeObject, BulletListObject, ImageObject]]

    class Config:
        json_schema_extra = {
            "example": {
                "list": [
                    {
                        "Heading": {
                            "id": "6728c4efdf839837d6b5b844",
                            "data": "Convolution Neural Network",
                            "htype": 1
                        }
                    },
                    {
                        "Image": {
                            "id": "669793df128074237bc4a790",
                            "uri": "https://cdn.torchend.com/meta_7acd082c23fe862fefeda08e"
                        }
                    },
                    {
                        "Paragraph": {
                            "id": "669f8a3f8fea995074f977ad",
                            "data": "Here is a basic NeuralNetwork built using Pytorch\nit uses nn.Module as Parent class"
                        }
                    },
                ]
            }
        }

class Page(BaseModel):
    p_id: str
    heading: str
    page_elements: List[Union[ParagraphObject, HeadingObject, CodeObject, BulletListObject, ImageObject]]

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
                "_id": {"oid": "66ab314b67082310f8c1dc4a"},
                "id": "369",
                "title": "Complete Rust-Backend Course",
                "pages": [
                    {
                        "p_id": "668014e8ad94a2476284f09d",
                        "heading": "Configure AWS S3",
                        "page_elements": [
                            {
                                "Heading": {
                                    "id": "6728c4efdf839837d6b5b844",
                                    "data": "Convolution Neural Network",
                                    "htype": 1
                                }
                            },
                            {
                                "Heading": {
                                    "id": "6728c77adf839837d6b5b847",
                                    "data": "Introduction",
                                    "htype": 2
                                }
                            },
                            {
                                "Code": {
                                    "id": "66bf7aee545b521aeaebb02f",
                                    "data": "pub async fn get_courses()->impl Responder{\n     match get_user_repository().await{\n          Ok()=>{\n               return HttpResponse::Ok()\n          },\n          Err()=>{\n               return HttpResponse::BadRequest()\n          }\n     }\n}",
                                    "lang": "rust"
                                }
                            },
                            {
                                "Heading": {
                                    "id": "66aa74d8a41ccc7f4df55bdb",
                                    "data": "Features",
                                    "htype": 2
                                }
                            },
                            {
                                "Image": {
                                    "id": "669793df128074237bc4a790",
                                    "uri": "https://cdn.torchend.com/meta_7acd082c23fe862fefeda08e"
                                }
                            },
                            {
                                "Paragraph": {
                                    "id": "669f8a3f8fea995074f977ad",
                                    "data": "Here is a basic NeuralNetwork built using Pytorch\nit uses nn.Module as Parent class"
                                }
                            },
                            {
                                "BulletList": {
                                    "id": "669179ba693714ddce85cd83",
                                    "lists": [
                                    {
                                        "id": "66923fe319bc07581ce3647b",
                                        "value": "Rust is a systems programming language that has gained significant attention and popularity since its inception.                                                            "
                                    },
                                    {
                                        "id": "66bcbb5903ac6c52820e3d8a",
                                        "value": "One of the standout features of Rust is its ownership system, which ensures memory safety without needing a garbage collector."
                                    },
                                    {
                                        "id": "669179d8693714ddce85cd85",
                                        "value": "Its primary design goals are safety, speed, and concurrency. Rust is syntactically similar to C++ but provides better memory safety while maintaining performance."
                                    },
                                    {
                                        "id": "66917a00693714ddce85cd87",
                                        "value": "This system enforces strict rules on how memory is managed, significantly reducing the likelihood of null pointer dereferences, buffer overflows, and data races."
                                    },
                                    {
                                        "id": "66bcbb6103ac6c52820e3d8b",
                                        "value": "Become super proficient in Rust to get job in companies like Anthropic,Microsoft,Openai,and Ola cabs."
                                    },
                                    {
                                        "id": "67147fbdbece8b4af9fa2bf7",
                                        "value": "Hai everyone this is bullet line number six..."
                                    }
                                    ]
                                }
                            },
                            {
                                "Image": {
                                    "id": "66cb593378a693fe12d2792d",
                                    "uri": "https://cdn.torchend.com/meta_c2b83f09f7f764cd902a3ba3"
                                }
                            },
                        ]
                    }
                ],
                "image_uri": "http://example.com/document-preview.png",
                "path": "complete-rust-backend-course",
                "publish": True
            }
        }

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

pageElements = {
    "Heading":HeadingObject,
    "Paragraph":ParagraphObject,
    "BulletList":BulletListObject,
    "Code":CodeObject,
    "Image":ImageObject
}
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
    message = f"Generate a {element_type} element about {content}."
    chat_history.append({"role":"user","content": content})
    try:
        completion = client.beta.chat.completions.parse(
            response_format=pageElements[element_type],
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
            # Convert the Document instance to a dictionary
            text_content_dict = text_content.model_dump()

            # Print the JSON response (for debugging purposes)
            print("JSON Response from OpenAI:", text_content_dict)  # You can also use logging

            # Generating image if image element
            if element_type == "Image":
                image_prompt = text_content.data
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
            
            # Creating a hash ID for element
            timestamp = int(time.time())
            text_content_data = text_content_dict[element_type]["data"]
            combined_data = f"{timestamp}:{text_content_data}"
            sha1_hash = hashlib.sha1(combined_data.encode()).hexdigest()

            # Truncate to the first 24 characters
            truncated_hash = sha1_hash[:24]

            print(truncated_hash)

            # Update the ID of the element
            text_content_dict[element_type]["id"] = truncated_hash

            # Append to chat history
            chat_history.append({"role": "assistant", "content": text_content_dict})

            return jsonify(success=True, message=text_content_dict)
        else:
            return jsonify(success=False, message="No text content found")
    except Exception as e:
        print(e)
        return jsonify(success=False, message=str(e)), 500
    
@app.route("/elements", methods=["POST",])
def generate_elements():
    content = request.json["message"]
    # print(content)
    message = content
    chat_history.append({"role":"user","content": content})
    try:
        completion = client.beta.chat.completions.parse(
            response_format=PageElements,
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a document generator platform. You will be given a topic and must generate an appropriate amount of page elements to describe the topic in the given structure."
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