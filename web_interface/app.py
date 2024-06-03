from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# Initialize OpenAI with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


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
                "content": f"Check if the following content is fully correct. If it is entirely positive correct, answer 'The information is correct.'. Otherwise, overwrite the corrected information instead the false information about content and do not add additional content:\n\n{content}",
            }
        ],
    )
    response_text = response.choices[0].message.content.strip()
    if "The information is correct." in response_text:
        return {
            "correct": "true",
            "message": "The information in the uploaded document is correct.",
            "result": response_text,
        }
    else:
        corrected_info = response_text.split("\n")
        return {
            "incorrect": "true",
            "message": "The information in the uploaded document is not entirely correct. Information has been corrected.",
            "result": [{"text": info} for info in corrected_info if info.strip()],
        }


if __name__ == "__main__":
    app.run(debug=True)
