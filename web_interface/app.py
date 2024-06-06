from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from openai import OpenAI
import os
import re

load_dotenv()

# Initialize OpenAI with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
ORIGINAL_TEXT = "Original:"
CORRECTED_TEXT = "Corrected:"


def convert_to_bold(text):
    # Use a regular expression to find text enclosed in double asterisks and replace it with HTML bold tags
    return re.sub(r"\*\*(.*?)\*\*", r'<strong style="color: red;">\1</strong>', text)


app.jinja_env.filters["bold"] = convert_to_bold


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))

    if file:
        try:
            content = file.read().decode("utf-8")
        except UnicodeDecodeError:
            try:
                content = file.read().decode("latin-1")
            except UnicodeDecodeError:
                content = file.read().decode("utf-8", errors="ignore")

        final_result = verify_document(content)
        return render_template("result.html", result=final_result)


def verify_document(content):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"Check if the following content is fully correct. If it is entirely positive and correct, answer 'The information is correct.'. Otherwise, give two texts, The first text shows 'Original:' with the given original text with each incorrect information highlighted by **text** and the second text shows 'Corrected:' the corrected information overwritten instead of the incorrect information and no ** in second corrected text and do not add additional content:\n\n{content}",
            }
        ],
    )
    response_text = response.choices[0].message.content.strip()

    print(response_text)

    if "The information is correct." in response_text:
        return {
            "correct": True,
            "message": "The information in the uploaded document is correct.",
            "result": response_text,
        }
    elif ORIGINAL_TEXT in response_text and CORRECTED_TEXT in response_text:
        original_text = ""
        corrected_text = ""
        if response_text.startswith(ORIGINAL_TEXT):
            original_text = (
                response_text.split(ORIGINAL_TEXT)[1].split(CORRECTED_TEXT)[0].strip()
            )
            corrected_text = response_text.split(CORRECTED_TEXT)[1].strip()
        else:
            original_text = (
                response_text.split(CORRECTED_TEXT)[1].split(ORIGINAL_TEXT)[0].strip()
            )
            corrected_text = response_text.split(ORIGINAL_TEXT)[1].strip()
        return {
            "incorrect": True,
            "message": "The information in the uploaded document is not entirely correct. Information has been corrected.",
            "result": {"original": original_text, "corrected": corrected_text},
        }
    else:
        return {
            "notFound": True,
            "message": "Didn't find relevant information",
        }


if __name__ == "__main__":
    app.run(debug=True)
