import random
from flask import Flask, jsonify

app = Flask(__name__)

OMIKUJI = [
    {
        "result": "大吉",
        "rank": 7,
        "color": "#c0392b",
        "accent": "#e74c3c",
        "emoji": "🌸",
        "overall": "この上ない幸運が舞い込む日。自信を持って新しい一歩を踏み出しましょう。",
        "love": "運命の出会いが近づいています。心を開いて。",
        "money": "思わぬ臨時収入あり。大切に使えばさらに福が続く。",
        "health": "心身ともに絶好調。無理せず喜びを分かち合って。",
        "work": "実力が認められ、周囲から信頼を集める日。",
    },
    {
        "result": "吉",
        "rank": 6,
        "color": "#8e44ad",
        "accent": "#9b59b6",
        "emoji": "✨",
        "overall": "良い流れに乗れる日。積極的に動けば道が開けます。",
        "love": "素直な気持ちを伝えることが吉。相手も同じ気持ち。",
        "money": "堅実な判断が実を結ぶ。焦らず着実に。",
        "health": "快調な日々が続く。リズムを崩さないよう心がけて。",
        "work": "アイデアが次々と浮かぶ。迷わず提案してみよう。",
    },
    {
        "result": "中吉",
        "rank": 5,
        "color": "#2471a3",
        "accent": "#2e86c1",
        "emoji": "🍀",
        "overall": "着実に前進できる日。地道な努力が必ず花を咲かせます。",
        "love": "関係が少しずつ深まっています。焦らず育んで。",
        "money": "計画的に使うことで余裕が生まれる。",
        "health": "普通に良好。軽い運動を取り入れると吉。",
        "work": "丁寧な仕事ぶりが評価されるとき。手を抜かずに。",
    },
    {
        "result": "小吉",
        "rank": 4,
        "color": "#1e8449",
        "accent": "#27ae60",
        "emoji": "🌿",
        "overall": "小さな喜びが積み重なる日。見逃さず感謝の心を持って。",
        "love": "日常の中にある小さな優しさを大切に。",
        "money": "大きな動きはないが、堅実さが安心を生む。",
        "health": "少し疲れ気味かも。早めの休息が薬。",
        "work": "細かい作業に集中力が出る。ミスなくこなして。",
    },
    {
        "result": "末吉",
        "rank": 3,
        "color": "#7d6608",
        "accent": "#d4ac0d",
        "emoji": "🌙",
        "overall": "今は力を蓄えるとき。静かに待てばやがて運が向いてきます。",
        "love": "今は自分を磨く期間。魅力が増せば縁も来る。",
        "money": "支出を抑えて堅実に。節約が次の幸運を呼ぶ。",
        "health": "体の声をよく聞いて。無理は禁物。",
        "work": "今は準備の時。学びを深めると後で活きる。",
    },
    {
        "result": "凶",
        "rank": 2,
        "color": "#616a6b",
        "accent": "#7f8c8d",
        "emoji": "🌧",
        "overall": "慎重に行動する日。小さなことに感謝し、謙虚に過ごしましょう。",
        "love": "誤解が生じやすい。言葉を選んで丁寧に伝えて。",
        "money": "衝動買いは禁物。今は守りに徹する時。",
        "health": "睡眠をしっかりとること。無理をすると後に響く。",
        "work": "慎重に確認しながら進めよう。焦りは禁物。",
    },
    {
        "result": "大凶",
        "rank": 1,
        "color": "#4a235a",
        "accent": "#6c3483",
        "emoji": "⚡",
        "overall": "試練の日。でも底を打てばあとは昇るのみ。今日の辛抱が明日の糧になります。",
        "love": "今は自分を見つめ直す好機。内面を磨けば必ず縁が来る。",
        "money": "新たな出費は先延ばしに。今あるものを大切に。",
        "health": "特に注意が必要な日。無理せずゆっくり休んで。",
        "work": "困難があっても諦めないで。乗り越えた先に成長がある。",
    },
]


@app.get("/")
def index():
    return HTML_PAGE


@app.get("/api/draw")
def draw():
    fortune = random.choice(OMIKUJI)
    return jsonify(fortune)


HTML_PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>おみくじ 3号 🌸</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;700;900&display=swap');

  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --accent: #c0392b;
    --petal: #f9c8d4;
    --bg-top: #fff5f8;
    --bg-bot: #fde8f0;
    --paper: #fffaf5;
    --ink: #2c1a1a;
    --gold: #b8860b;
  }

  html, body {
    height: 100%;
  }

  body {
    font-family: 'Noto Serif JP', "Hiragino Mincho ProN", "Yu Mincho", serif;
    background: linear-gradient(160deg, var(--bg-top) 0%, var(--bg-bot) 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    position: relative;
  }

  /* ===== Sakura canvas ===== */
  #sakuraCanvas {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
  }

  /* ===== Main container ===== */
  .container {
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 2rem 1rem;
    width: 100%;
    max-width: 480px;
  }

  .site-title {
    font-size: 1.6rem;
    font-weight: 900;
    color: var(--accent);
    letter-spacing: 0.5em;
    margin-bottom: 0.3rem;
    text-shadow: 1px 1px 0 rgba(192,57,43,0.2);
  }
  .site-sub {
    font-size: 0.85rem;
    color: #a07060;
    letter-spacing: 0.3em;
    margin-bottom: 2.5rem;
  }

  /* ===== Draw phase ===== */
  #drawPhase { }

  .fortune-tube {
    width: 100px;
    height: 180px;
    margin: 0 auto 2rem;
    position: relative;
    cursor: pointer;
    filter: drop-shadow(0 8px 20px rgba(192,57,43,0.25));
    transition: transform 0.2s;
  }
  .fortune-tube:hover { transform: scale(1.05) translateY(-4px); }
  .fortune-tube.shaking {
    animation: tubeShake 0.12s infinite;
  }
  @keyframes tubeShake {
    0%   { transform: rotate(-4deg) translateY(0); }
    25%  { transform: rotate(4deg) translateY(-3px); }
    50%  { transform: rotate(-3deg) translateY(0); }
    75%  { transform: rotate(3deg) translateY(-2px); }
    100% { transform: rotate(-4deg) translateY(0); }
  }

  .tube-body {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #c0392b 0%, #922b21 50%, #c0392b 100%);
    border-radius: 50% 50% 20% 20% / 20% 20% 10% 10%;
    border: 2px solid #922b21;
    position: relative;
    overflow: hidden;
    box-shadow: inset -6px 0 12px rgba(0,0,0,0.2), inset 6px 0 12px rgba(255,255,255,0.1);
  }
  .tube-kanji {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    writing-mode: vertical-rl;
    font-size: 1.5rem;
    font-weight: 900;
    color: #ffd700;
    letter-spacing: 0.3em;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
  }
  .tube-rim {
    position: absolute;
    top: 0;
    left: -2px;
    right: -2px;
    height: 20px;
    background: linear-gradient(180deg, #ffd700, #b8860b);
    border-radius: 50%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  }

  /* Sticks peeking out */
  .sticks {
    position: absolute;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 5px;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .fortune-tube.shaking .sticks { opacity: 1; }
  .stick {
    width: 5px;
    height: 40px;
    background: linear-gradient(180deg, #deb887, #c4a265);
    border-radius: 2px 2px 0 0;
  }
  .stick:nth-child(1) { transform: rotate(-10deg) translateY(3px); animation: stickBob1 0.2s infinite alternate; }
  .stick:nth-child(2) { animation: stickBob2 0.2s infinite alternate; }
  .stick:nth-child(3) { transform: rotate(10deg) translateY(3px); animation: stickBob1 0.2s infinite alternate reverse; }
  @keyframes stickBob1 { from { transform: rotate(-10deg) translateY(3px); } to { transform: rotate(-10deg) translateY(-5px); } }
  @keyframes stickBob2 { from { transform: translateY(0); } to { transform: translateY(-8px); } }

  .draw-hint {
    font-size: 1rem;
    color: #a07060;
    letter-spacing: 0.25em;
    animation: breathe 2.5s ease-in-out infinite;
  }
  @keyframes breathe {
    0%, 100% { opacity: 0.5; transform: translateY(0); }
    50% { opacity: 1; transform: translateY(-3px); }
  }

  /* ===== Flip reveal ===== */
  .card-scene {
    width: 320px;
    height: 440px;
    margin: 0 auto 1.5rem;
    perspective: 1200px;
    display: none;
  }
  .card-scene.visible { display: block; }

  .card-inner {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    transform: rotateY(180deg);
    transition: transform 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .card-inner.flipped { transform: rotateY(0deg); }

  .card-face {
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    border-radius: 20px;
    overflow: hidden;
  }

  /* Card back */
  .card-back {
    background: linear-gradient(135deg, #922b21, #c0392b, #922b21);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid #ffd700;
    box-shadow: 0 12px 40px rgba(192,57,43,0.4);
    transform: rotateY(180deg);
  }
  .card-back-text {
    writing-mode: vertical-rl;
    font-size: 2rem;
    font-weight: 900;
    color: #ffd700;
    letter-spacing: 0.4em;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
  }

  /* Card front */
  .card-front {
    background: var(--paper);
    border: 3px solid var(--accent);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 1.5rem 1.2rem;
    position: relative;
  }
  .card-front::before {
    content: '';
    position: absolute;
    inset: 8px;
    border: 1px solid rgba(192,57,43,0.2);
    border-radius: 14px;
    pointer-events: none;
  }

  /* Washi pattern overlay */
  .card-front::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 19px, rgba(192,57,43,0.04) 20px),
      repeating-linear-gradient(90deg, transparent, transparent 19px, rgba(192,57,43,0.04) 20px);
    pointer-events: none;
    border-radius: 17px;
  }

  .card-header {
    font-size: 0.75rem;
    color: var(--gold);
    letter-spacing: 0.4em;
    margin-bottom: 0.8rem;
    position: relative;
    z-index: 1;
  }

  .result-emoji {
    font-size: 2.5rem;
    margin-bottom: 0.4rem;
    position: relative;
    z-index: 1;
    animation: floatEmoji 3s ease-in-out infinite;
  }
  @keyframes floatEmoji {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-6px) rotate(5deg); }
  }

  .result-main {
    font-size: 4.5rem;
    font-weight: 900;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 0.4rem;
    position: relative;
    z-index: 1;
    text-shadow: 2px 2px 0 rgba(192,57,43,0.15);
    opacity: 0;
    transform: scale(0.5);
    transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .result-main.show { opacity: 1; transform: scale(1); }

  .result-overall {
    font-size: 0.9rem;
    color: #5a3a2a;
    line-height: 1.9;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.5s ease 0.4s, transform 0.5s ease 0.4s;
  }
  .result-overall.show { opacity: 1; transform: translateY(0); }

  /* Category grid */
  .categories {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    position: relative;
    z-index: 1;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.5s ease 0.7s, transform 0.5s ease 0.7s;
  }
  .categories.show { opacity: 1; transform: translateY(0); }

  .cat-item {
    background: rgba(192,57,43,0.06);
    border: 1px solid rgba(192,57,43,0.2);
    border-radius: 10px;
    padding: 0.6rem 0.5rem;
    text-align: left;
  }
  .cat-label {
    font-size: 0.65rem;
    color: var(--gold);
    letter-spacing: 0.2em;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 0.3rem;
  }
  .cat-text {
    font-size: 0.72rem;
    color: #5a3a2a;
    line-height: 1.6;
  }

  /* ===== Retry button ===== */
  .retry-btn {
    display: inline-block;
    padding: 0.85rem 2.4rem;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 50px;
    font-size: 1rem;
    font-family: inherit;
    cursor: pointer;
    letter-spacing: 0.2em;
    box-shadow: 0 4px 16px rgba(192,57,43,0.35);
    transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
    opacity: 0;
    transition: opacity 0.5s ease 1s, transform 0.2s, box-shadow 0.2s;
  }
  .retry-btn.show { opacity: 1; }
  .retry-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(192,57,43,0.45); }
  .retry-btn:active { transform: translateY(0); }

  /* ===== Flash overlay ===== */
  .flash {
    position: fixed;
    inset: 0;
    background: #fff;
    opacity: 0;
    z-index: 50;
    pointer-events: none;
  }
  .flash.bang {
    animation: flashOut 0.7s ease-out forwards;
  }
  @keyframes flashOut {
    0% { opacity: 0.85; }
    100% { opacity: 0; }
  }
</style>
</head>
<body>

<canvas id="sakuraCanvas"></canvas>
<div class="flash" id="flash"></div>

<div class="container">
  <div class="site-title">⛩ おみくじ 3号 ⛩</div>
  <div class="site-sub">〜 桜花みくじ 〜</div>

  <!-- Draw phase -->
  <div id="drawPhase">
    <div class="fortune-tube" id="fortuneTube" onclick="startDraw()">
      <div class="sticks">
        <div class="stick"></div>
        <div class="stick"></div>
        <div class="stick"></div>
      </div>
      <div class="tube-body">
        <div class="tube-rim"></div>
        <div class="tube-kanji">御神籤</div>
      </div>
    </div>
    <div class="draw-hint">🌸 タップして運勢を授かる 🌸</div>
  </div>

  <!-- Result card (flip) -->
  <div class="card-scene" id="cardScene">
    <div class="card-inner" id="cardInner">
      <!-- back -->
      <div class="card-face card-back">
        <div class="card-back-text">御神籤</div>
      </div>
      <!-- front -->
      <div class="card-face card-front">
        <div class="card-header">— 本日の運勢 —</div>
        <div class="result-emoji" id="resultEmoji"></div>
        <div class="result-main" id="resultMain"></div>
        <div class="result-overall" id="resultOverall"></div>
        <div class="categories" id="categories">
          <div class="cat-item">
            <div class="cat-label">💕 恋愛</div>
            <div class="cat-text" id="catLove"></div>
          </div>
          <div class="cat-item">
            <div class="cat-label">💰 金運</div>
            <div class="cat-text" id="catMoney"></div>
          </div>
          <div class="cat-item">
            <div class="cat-label">🌿 健康</div>
            <div class="cat-text" id="catHealth"></div>
          </div>
          <div class="cat-item">
            <div class="cat-label">💼 仕事</div>
            <div class="cat-text" id="catWork"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <button class="retry-btn" id="retryBtn" onclick="resetDraw()">もう一度引く 🌸</button>
</div>

<script>
// ===== Sakura petals =====
const canvas = document.getElementById('sakuraCanvas');
const ctx = canvas.getContext('2d');
let petals = [];

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

function randomPetal() {
  return {
    x: Math.random() * canvas.width,
    y: -20,
    r: 5 + Math.random() * 8,
    vx: (Math.random() - 0.5) * 1.5,
    vy: 0.8 + Math.random() * 1.5,
    angle: Math.random() * Math.PI * 2,
    spin: (Math.random() - 0.5) * 0.05,
    opacity: 0.6 + Math.random() * 0.4,
    color: ['#f9c8d4', '#f4a7b9', '#fde2ec', '#f7c5d5'][Math.floor(Math.random() * 4)],
  };
}

function drawPetal(p) {
  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(p.angle);
  ctx.globalAlpha = p.opacity;
  ctx.beginPath();
  ctx.ellipse(0, 0, p.r, p.r * 0.55, 0, 0, Math.PI * 2);
  ctx.fillStyle = p.color;
  ctx.fill();
  ctx.restore();
}

function animatePetals() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  petals.forEach(p => {
    p.x += p.vx + Math.sin(p.angle * 2) * 0.4;
    p.y += p.vy;
    p.angle += p.spin;
    drawPetal(p);
  });
  petals = petals.filter(p => p.y < canvas.height + 30);
  if (Math.random() < 0.15) petals.push(randomPetal());
  requestAnimationFrame(animatePetals);
}

// Burst of petals on reveal
function burstPetals(count) {
  for (let i = 0; i < count; i++) {
    const p = randomPetal();
    p.y = canvas.height * 0.3 + Math.random() * canvas.height * 0.3;
    p.vy = -(3 + Math.random() * 5);
    p.vx = (Math.random() - 0.5) * 6;
    petals.push(p);
  }
}

animatePetals();

// ===== Draw logic =====
let isDrawing = false;
let currentFortune = null;

async function startDraw() {
  if (isDrawing) return;
  isDrawing = true;

  const tube = document.getElementById('fortuneTube');
  tube.classList.add('shaking');

  // Fetch fortune
  const res = await fetch('/api/draw');
  currentFortune = await res.json();

  // Apply accent color
  document.documentElement.style.setProperty('--accent', currentFortune.color);

  await sleep(1600);

  tube.classList.remove('shaking');

  // Flash
  const flash = document.getElementById('flash');
  flash.classList.add('bang');
  setTimeout(() => flash.classList.remove('bang'), 700);

  await sleep(200);

  // Hide draw phase, show card
  document.getElementById('drawPhase').style.display = 'none';

  const scene = document.getElementById('cardScene');
  scene.classList.add('visible');
  scene.style.borderColor = currentFortune.color;

  // Burst petals
  burstPetals(40);

  // Flip card after short delay
  await sleep(300);
  const inner = document.getElementById('cardInner');
  inner.classList.add('flipped');

  // Populate content during flip
  document.getElementById('resultEmoji').textContent = currentFortune.emoji;
  document.getElementById('catLove').textContent = currentFortune.love;
  document.getElementById('catMoney').textContent = currentFortune.money;
  document.getElementById('catHealth').textContent = currentFortune.health;
  document.getElementById('catWork').textContent = currentFortune.work;

  document.getElementById('resultMain').textContent = currentFortune.result;
  document.getElementById('resultOverall').textContent = currentFortune.overall;
  document.getElementById('cardScene').querySelector('.card-front').style.borderColor = currentFortune.color;
  document.getElementById('cardScene').querySelector('.card-front').style.setProperty('--accent', currentFortune.color);

  // Stagger text reveals
  await sleep(700);
  document.getElementById('resultMain').classList.add('show');

  await sleep(350);
  document.getElementById('resultOverall').classList.add('show');

  await sleep(300);
  document.getElementById('categories').classList.add('show');

  await sleep(500);
  document.getElementById('retryBtn').classList.add('show');

  // Extra petals for top fortunes
  if (currentFortune.rank >= 6) {
    setTimeout(() => burstPetals(60), 500);
    setTimeout(() => burstPetals(40), 1200);
  }

  isDrawing = false;
}

function resetDraw() {
  // Reset all states
  document.documentElement.style.setProperty('--accent', '#c0392b');

  const inner = document.getElementById('cardInner');
  inner.style.transition = 'none';
  inner.classList.remove('flipped');
  void inner.offsetWidth; // reflow
  inner.style.transition = '';

  document.getElementById('resultMain').classList.remove('show');
  document.getElementById('resultOverall').classList.remove('show');
  document.getElementById('categories').classList.remove('show');
  document.getElementById('retryBtn').classList.remove('show');

  document.getElementById('cardScene').classList.remove('visible');
  document.getElementById('drawPhase').style.display = '';
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
</script>
</body>
</html>"""


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
