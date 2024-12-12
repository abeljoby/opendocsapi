from flask import Flask, flash, render_template, request
from openai import OpenAI


def create_app():
    app = Flask(__name__)

    client = OpenAI()

    @app.route("/", methods=['GET','POST'])
    @app.route("/<name>", methods=['GET','POST'])
    def prompt(name=None):
        if request.method == 'POST':
            error = None
            prompt = request.form['prompt']
            if not prompt:
                error = "A prompt is required!"
            if error is not None:
                send_prompt(prompt)
            flash(error)
        return render_template("index.html",person=name)

    return app
