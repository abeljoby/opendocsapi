from flask import Flask, flash, render_template, request, jsonify
from openai import OpenAI
import os

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
