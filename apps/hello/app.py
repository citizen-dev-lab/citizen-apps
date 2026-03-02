from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return "hello from claude 🚀🚀🚀🚀"

if __name__ == "__main__":
    # Cloud RunはPORT環境変数で指定してくる
    import os
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
