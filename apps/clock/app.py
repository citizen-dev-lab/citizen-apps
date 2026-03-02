from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clock</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #1a1a2e;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #eee;
  }
  .clock {
    text-align: center;
  }
  #time {
    font-size: min(20vw, 8rem);
    font-weight: 200;
    letter-spacing: 0.05em;
  }
  #date {
    margin-top: 0.5rem;
    font-size: min(5vw, 1.5rem);
    color: #aaa;
  }
</style>
</head>
<body>
<div class="clock">
  <div id="time"></div>
  <div id="date"></div>
</div>
<script>
function update() {
  const now = new Date();
  const opt = { timeZone: 'Asia/Tokyo' };
  document.getElementById('time').textContent =
    now.toLocaleTimeString('ja-JP', { ...opt, hour: '2-digit', minute: '2-digit', second: '2-digit' });
  document.getElementById('date').textContent =
    now.toLocaleDateString('ja-JP', { ...opt, year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' });
}
update();
setInterval(update, 1000);
</script>
</body>
</html>"""


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
