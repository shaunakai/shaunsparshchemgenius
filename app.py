from flask import Flask, request, jsonify, send_file
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

@app.route("/")
def index():
    # Serve the HTML file
    return send_file("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)