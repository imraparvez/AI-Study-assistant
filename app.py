from flask import Flask, render_template, request, jsonify
import ollama
from pypdf import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        question = request.form.get("question", "")

        pdf_text = ""
        image_path = None

        # PDF Upload
        if "pdf" in request.files:

            pdf_file = request.files["pdf"]

            if pdf_file.filename != "":

                pdf_path = os.path.join(
                    UPLOAD_FOLDER,
                    pdf_file.filename
                )

                pdf_file.save(pdf_path)

                reader = PdfReader(pdf_path)

                for page in reader.pages:

                    text = page.extract_text()

                    if text:
                        pdf_text += text + "\n"

        # Image Upload
        if "image" in request.files:

            image_file = request.files["image"]

            if image_file.filename != "":

                image_path = os.path.join(
                    UPLOAD_FOLDER,
                    image_file.filename
                )

                image_file.save(image_path)

        # If image exists -> use Llava
        if image_path:

            response = ollama.chat(
                model="llava",
                messages=[
                    {
                        "role": "user",
                        "content": question,
                        "images": [image_path]
                    }
                ]
            )

            answer = response["message"]["content"]

        else:

            prompt = f"""
You are an AI Study Assistant.

Use the PDF content if available.

PDF Content:
{pdf_text}

Question:
{question}

Give a detailed answer suitable for a student.
"""

            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "answer": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)