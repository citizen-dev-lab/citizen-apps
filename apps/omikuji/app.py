import random
from flask import Flask

app = Flask(__name__)

OMIKUJI = [
    {
        "result": "大吉",
        "message": "最高の運勢です！何をやってもうまくいく日。",
        "color": "#e60033",
    },
    {
        "result": "吉",
        "message": "良い運勢です。積極的に行動しましょう。",
        "color": "#e95464",
    },
    {
        "result": "中吉",
        "message": "まずまずの運勢。コツコツ努力が実を結びます。",
        "color": "#f19072",
    },
    {
        "result": "小吉",
        "message": "小さな幸せが訪れます。見逃さないで。",
        "color": "#f6ad49",
    },
    {
        "result": "末吉",
        "message": "今は静かに待つとき。やがて運が開けます。",
        "color": "#928178",
    },
    {
        "result": "凶",
        "message": "慎重に過ごしましょう。無理は禁物です。",
        "color": "#6a5d7b",
    },
    {
        "result": "大凶",
        "message": "今日は厄払いの日。明日からは上がるのみ！",
        "color": "#4a4458",
    },
]


@app.get("/")
def index():
    fortune = random.choice(OMIKUJI)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>おみくじ</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "Hiragino Mincho ProN", "Yu Mincho", serif;
    background: #fdf5e6;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .container {{
    text-align: center;
    padding: 2rem;
  }}
  h1 {{
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 2rem;
    letter-spacing: 0.3em;
  }}
  .ofuda {{
    background: #fff;
    border: 3px solid {fortune["color"]};
    border-radius: 12px;
    padding: 2.5rem 3rem;
    margin: 0 auto 2rem;
    max-width: 280px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  }}
  .result {{
    font-size: 4rem;
    font-weight: bold;
    color: {fortune["color"]};
    margin-bottom: 1rem;
  }}
  .message {{
    font-size: 1.1rem;
    color: #555;
    line-height: 1.8;
  }}
  .btn {{
    display: inline-block;
    padding: 0.8rem 2rem;
    background: {fortune["color"]};
    color: #fff;
    text-decoration: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-family: inherit;
    transition: opacity 0.2s;
  }}
  .btn:hover {{ opacity: 0.8; }}
</style>
</head>
<body>
<div class="container">
  <h1>⛩ おみくじ ⛩</h1>
  <div class="ofuda">
    <div class="result">{fortune["result"]}</div>
    <div class="message">{fortune["message"]}</div>
  </div>
  <a href="/" class="btn">もう一度引く</a>
</div>
</body>
</html>"""


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
