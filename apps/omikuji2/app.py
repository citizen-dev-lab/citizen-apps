import json
import random

from flask import Flask, jsonify

app = Flask(__name__)

OMIKUJI = [
    {
        "result": "大吉",
        "message": "最高の運勢です！何をやってもうまくいく日。自信を持って突き進みましょう！",
        "color": "#e60033",
        "rank": 7,
        "emoji": "🌟",
        "sub": "全てが輝く最高の一日",
    },
    {
        "result": "吉",
        "message": "良い運勢です。積極的に行動すれば、道が開けます。",
        "color": "#e95464",
        "rank": 6,
        "emoji": "✨",
        "sub": "幸運の風が吹いている",
    },
    {
        "result": "中吉",
        "message": "まずまずの運勢。コツコツ努力が実を結びます。",
        "color": "#f08300",
        "rank": 5,
        "emoji": "🔥",
        "sub": "努力が報われるとき",
    },
    {
        "result": "小吉",
        "message": "小さな幸せが訪れます。見逃さないようにしましょう。",
        "color": "#f6ad49",
        "rank": 4,
        "emoji": "🍀",
        "sub": "ささやかな喜びの日",
    },
    {
        "result": "末吉",
        "message": "今は静かに待つとき。やがて運が開けます。",
        "color": "#928178",
        "rank": 3,
        "emoji": "🌙",
        "sub": "静かに力を蓄えよう",
    },
    {
        "result": "凶",
        "message": "慎重に過ごしましょう。無理は禁物です。",
        "color": "#6a5d7b",
        "rank": 2,
        "emoji": "💨",
        "sub": "嵐の前の静けさ",
    },
    {
        "result": "大凶",
        "message": "今日は厄払いの日。明日からは上がるのみ！",
        "color": "#4a4458",
        "rank": 1,
        "emoji": "⚡",
        "sub": "底を打てばあとは昇るだけ",
    },
]


@app.get("/")
def index():
    return HTML_PAGE


@app.get("/api/draw")
def draw():
    fortune = random.choice(OMIKUJI)
    return jsonify(fortune)


HTML_PAGE = (
    """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>おみくじ 2号 🎆</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700;900&display=swap');

  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --accent: #e60033;
    --bg: #0a0a1a;
    --bg2: #12122a;
  }

  body {
    font-family: 'Noto Serif JP', serif;
    background: var(--bg);
    color: #fff;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }

  /* === Background stars === */
  .stars {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
  }
  .star {
    position: absolute;
    width: 2px;
    height: 2px;
    background: #fff;
    border-radius: 50%;
    animation: twinkle 3s ease-in-out infinite alternate;
  }
  @keyframes twinkle {
    0% { opacity: 0.2; transform: scale(1); }
    100% { opacity: 1; transform: scale(1.5); }
  }

  /* === Canvas for particles === */
  #particleCanvas {
    position: fixed;
    inset: 0;
    z-index: 5;
    pointer-events: none;
  }

  /* === Main container === */
  .container {
    text-align: center;
    z-index: 10;
    position: relative;
  }

  h1 {
    font-size: 1.8rem;
    color: #ffd700;
    margin-bottom: 1.5rem;
    letter-spacing: 0.4em;
    text-shadow: 0 0 20px rgba(255,215,0,0.5);
  }

  /* === Omikuji box (initial state) === */
  .omikuji-box {
    width: 220px;
    height: 300px;
    margin: 0 auto 2rem;
    position: relative;
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  .omikuji-box:hover { transform: scale(1.05); }
  .omikuji-box.shaking {
    animation: violentShake 0.1s infinite;
  }

  .box-body {
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #8b0000 0%, #cc0000 30%, #8b0000 100%);
    border-radius: 20px 20px 8px 8px;
    border: 3px solid #ffd700;
    position: relative;
    box-shadow: 0 0 40px rgba(255,0,0,0.3), inset 0 0 30px rgba(0,0,0,0.3);
    overflow: hidden;
  }
  .box-body::before {
    content: '御神籤';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 2.2rem;
    font-weight: 900;
    color: #ffd700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    writing-mode: vertical-rl;
    letter-spacing: 0.3em;
  }
  .box-hole {
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 30px;
    height: 30px;
    background: #1a0000;
    border-radius: 50%;
    border: 2px solid #ffd700;
  }
  .stick {
    position: absolute;
    top: -40px;
    left: 50%;
    transform: translateX(-50%);
    width: 6px;
    height: 60px;
    background: linear-gradient(180deg, #deb887, #d2a860);
    border-radius: 3px 3px 0 0;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .omikuji-box.shaking .stick {
    opacity: 1;
    animation: stickPop 0.15s infinite alternate;
  }

  @keyframes violentShake {
    0% { transform: translate(-3px, -2px) rotate(-2deg); }
    25% { transform: translate(3px, 1px) rotate(2deg); }
    50% { transform: translate(-2px, 2px) rotate(-1deg); }
    75% { transform: translate(2px, -1px) rotate(1deg); }
    100% { transform: translate(-1px, -2px) rotate(-2deg); }
  }
  @keyframes stickPop {
    from { top: -40px; }
    to { top: -55px; }
  }

  .draw-text {
    font-size: 1.2rem;
    color: #ffd700;
    letter-spacing: 0.2em;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
  }

  /* === Light beam === */
  .light-burst {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    z-index: 8;
    pointer-events: none;
  }
  .light-beam {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 4px;
    height: 200vh;
    transform-origin: center top;
    opacity: 0;
  }
  .light-burst.active .light-beam {
    animation: beamBlast 1.5s ease-out forwards;
  }
  @keyframes beamBlast {
    0% { opacity: 0; height: 0; }
    20% { opacity: 0.8; height: 200vh; }
    100% { opacity: 0; height: 200vh; }
  }

  /* === Flash overlay === */
  .flash-overlay {
    position: fixed;
    inset: 0;
    background: #fff;
    z-index: 15;
    opacity: 0;
    pointer-events: none;
    transition: none;
  }
  .flash-overlay.flash {
    animation: flashBang 0.8s ease-out forwards;
  }
  @keyframes flashBang {
    0% { opacity: 1; }
    100% { opacity: 0; }
  }

  /* === Result card === */
  .result-area {
    display: none;
    perspective: 1000px;
  }
  .result-area.visible {
    display: block;
  }

  .result-card {
    width: 300px;
    margin: 0 auto 1.5rem;
    padding: 2.5rem 2rem;
    background: rgba(255,255,255,0.05);
    border: 3px solid var(--accent);
    border-radius: 16px;
    position: relative;
    overflow: hidden;
    transform: scale(0) rotateY(180deg);
    box-shadow: 0 0 60px rgba(255,255,255,0.1);
  }
  .result-card.reveal {
    animation: cardReveal 1s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  }
  @keyframes cardReveal {
    0% { transform: scale(0) rotateY(180deg); }
    60% { transform: scale(1.1) rotateY(0deg); }
    80% { transform: scale(0.95) rotateY(0deg); }
    100% { transform: scale(1) rotateY(0deg); }
  }

  .result-card::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 16px;
    background: conic-gradient(from 0deg, transparent, var(--accent), transparent, var(--accent), transparent);
    z-index: -1;
    animation: borderSpin 3s linear infinite;
  }
  @keyframes borderSpin {
    to { transform: rotate(360deg); }
  }

  .result-card .glow {
    position: absolute;
    inset: 0;
    border-radius: 16px;
    box-shadow: inset 0 0 60px rgba(255,255,255,0.1);
    pointer-events: none;
  }

  .result-emoji {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    animation: emojiFloat 2s ease-in-out infinite;
  }
  @keyframes emojiFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  .result-text {
    font-size: 5rem;
    font-weight: 900;
    color: var(--accent);
    text-shadow: 0 0 40px var(--accent), 0 0 80px var(--accent);
    margin-bottom: 0.3rem;
    opacity: 0;
  }
  .result-text.show {
    animation: textDramatic 0.8s ease-out forwards;
  }
  @keyframes textDramatic {
    0% { opacity: 0; transform: scale(3); filter: blur(10px); }
    60% { opacity: 1; transform: scale(0.9); filter: blur(0); }
    80% { transform: scale(1.05); }
    100% { opacity: 1; transform: scale(1); filter: blur(0); }
  }

  .result-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.6);
    margin-bottom: 1rem;
    opacity: 0;
  }
  .result-sub.show {
    animation: fadeUp 0.6s ease-out 0.3s forwards;
  }

  .result-message {
    font-size: 1.15rem;
    color: rgba(255,255,255,0.85);
    line-height: 1.9;
    opacity: 0;
  }
  .result-message.show {
    animation: fadeUp 0.6s ease-out 0.5s forwards;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* === Retry button === */
  .retry-btn {
    display: inline-block;
    padding: 1rem 2.5rem;
    background: transparent;
    color: #ffd700;
    border: 2px solid #ffd700;
    border-radius: 50px;
    font-size: 1.1rem;
    font-family: inherit;
    cursor: pointer;
    letter-spacing: 0.15em;
    transition: all 0.3s;
    opacity: 0;
    text-decoration: none;
  }
  .retry-btn.show {
    animation: fadeUp 0.6s ease-out 0.8s forwards;
  }
  .retry-btn:hover {
    background: #ffd700;
    color: #0a0a1a;
    box-shadow: 0 0 30px rgba(255,215,0,0.4);
  }

  /* === Floating kanji === */
  .floating-kanji {
    position: fixed;
    font-size: 3rem;
    opacity: 0;
    pointer-events: none;
    z-index: 4;
    color: rgba(255,255,255,0.15);
  }
  .floating-kanji.rise {
    animation: kanjiRise 4s ease-out forwards;
  }
  @keyframes kanjiRise {
    0% { opacity: 0; transform: translateY(100vh) rotate(0deg) scale(0.5); }
    30% { opacity: 0.3; }
    100% { opacity: 0; transform: translateY(-100vh) rotate(360deg) scale(1.5); }
  }

  /* === Screen shake === */
  body.screen-shake {
    animation: screenShake 0.5s ease-out;
  }
  @keyframes screenShake {
    0% { transform: translate(0,0); }
    10% { transform: translate(-8px, -5px); }
    20% { transform: translate(8px, 5px); }
    30% { transform: translate(-6px, 4px); }
    40% { transform: translate(6px, -4px); }
    50% { transform: translate(-4px, 3px); }
    60% { transform: translate(4px, -2px); }
    70% { transform: translate(-2px, 2px); }
    80% { transform: translate(2px, -1px); }
    90% { transform: translate(-1px, 1px); }
    100% { transform: translate(0,0); }
  }
</style>
</head>
<body>

<!-- Background stars -->
<div class="stars" id="stars"></div>

<!-- Particle canvas -->
<canvas id="particleCanvas"></canvas>

<!-- Light beams -->
<div class="light-burst" id="lightBurst"></div>

<!-- Flash -->
<div class="flash-overlay" id="flash"></div>

<!-- Main content -->
<div class="container">
  <h1>⛩ おみくじ 2号 ⛩</h1>

  <!-- Draw phase -->
  <div id="drawPhase">
    <div class="omikuji-box" id="omikujiBox" onclick="startDraw()">
      <div class="box-body">
        <div class="box-hole"></div>
        <div class="stick" id="stick"></div>
      </div>
    </div>
    <div class="draw-text">▲ タップしておみくじを引く ▲</div>
  </div>

  <!-- Result phase -->
  <div class="result-area" id="resultArea">
    <div class="result-card" id="resultCard">
      <div class="glow"></div>
      <div class="result-emoji" id="resultEmoji"></div>
      <div class="result-text" id="resultText"></div>
      <div class="result-sub" id="resultSub"></div>
      <div class="result-message" id="resultMessage"></div>
    </div>
    <button class="retry-btn" id="retryBtn" onclick="resetDraw()">もう一度引く</button>
  </div>
</div>

<script>
// --- Star background ---
(function initStars() {
  const container = document.getElementById('stars');
  for (let i = 0; i < 80; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    star.style.left = Math.random() * 100 + '%';
    star.style.top = Math.random() * 100 + '%';
    star.style.animationDelay = (Math.random() * 3) + 's';
    star.style.animationDuration = (2 + Math.random() * 3) + 's';
    container.appendChild(star);
  }
})();

// --- Particle system ---
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');
let particles = [];
let animFrame;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

class Particle {
  constructor(x, y, color, type) {
    this.x = x;
    this.y = y;
    this.color = color;
    this.type = type;
    this.life = 1;
    this.decay = 0.008 + Math.random() * 0.015;

    if (type === 'firework') {
      const angle = Math.random() * Math.PI * 2;
      const speed = 2 + Math.random() * 6;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed;
      this.size = 2 + Math.random() * 3;
      this.gravity = 0.05;
    } else if (type === 'confetti') {
      this.vx = (Math.random() - 0.5) * 8;
      this.vy = -5 - Math.random() * 10;
      this.size = 4 + Math.random() * 6;
      this.gravity = 0.15;
      this.rotation = Math.random() * 360;
      this.rotSpeed = (Math.random() - 0.5) * 15;
      this.width = 3 + Math.random() * 5;
      this.height = 6 + Math.random() * 10;
    } else if (type === 'spark') {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1 + Math.random() * 3;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed;
      this.size = 1 + Math.random() * 2;
      this.gravity = 0.02;
    }
  }

  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.vy += this.gravity;
    this.life -= this.decay;
    if (this.type === 'confetti') {
      this.rotation += this.rotSpeed;
    }
  }

  draw(ctx) {
    ctx.save();
    ctx.globalAlpha = Math.max(0, this.life);

    if (this.type === 'confetti') {
      ctx.translate(this.x, this.y);
      ctx.rotate((this.rotation * Math.PI) / 180);
      ctx.fillStyle = this.color;
      ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
    } else {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * this.life, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.shadowBlur = 15;
      ctx.shadowColor = this.color;
      ctx.fill();
    }
    ctx.restore();
  }
}

function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles = particles.filter(p => p.life > 0);
  particles.forEach(p => { p.update(); p.draw(ctx); });
  if (particles.length > 0) {
    animFrame = requestAnimationFrame(animateParticles);
  }
}

function spawnFirework(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    particles.push(new Particle(x, y, color, 'firework'));
  }
  if (!animFrame || particles.length === count) {
    animateParticles();
  }
}

function spawnConfetti(count) {
  const colors = ['#ff0000','#ffd700','#00ff88','#00aaff','#ff44ff','#ff8800','#ffffff'];
  for (let i = 0; i < count; i++) {
    const x = Math.random() * canvas.width;
    const y = canvas.height * 0.3 + Math.random() * canvas.height * 0.2;
    const c = colors[Math.floor(Math.random() * colors.length)];
    particles.push(new Particle(x, y, c, 'confetti'));
  }
  if (!animFrame || particles.length === count) {
    animateParticles();
  }
}

function spawnSparks(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    particles.push(new Particle(x, y, color, 'spark'));
  }
  if (!animFrame || particles.length === count) {
    animateParticles();
  }
}

// --- Light beams ---
function triggerLightBeams(color) {
  const burst = document.getElementById('lightBurst');
  burst.innerHTML = '';
  const numBeams = 16;
  for (let i = 0; i < numBeams; i++) {
    const beam = document.createElement('div');
    beam.className = 'light-beam';
    beam.style.transform = `rotate(${(360 / numBeams) * i}deg)`;
    beam.style.background = `linear-gradient(to top, ${color}, transparent)`;
    beam.style.animationDelay = `${i * 0.03}s`;
    burst.appendChild(beam);
  }
  burst.classList.add('active');
  setTimeout(() => { burst.classList.remove('active'); burst.innerHTML = ''; }, 2000);
}

// --- Floating kanji ---
function spawnFloatingKanji(text) {
  const kanjiChars = ['福', '寿', '喜', '幸', '運', '吉', '祝', '縁', '夢', '光', '愛', '和'];
  const chars = text ? [text] : kanjiChars;
  for (let i = 0; i < 12; i++) {
    const el = document.createElement('div');
    el.className = 'floating-kanji';
    el.textContent = chars[Math.floor(Math.random() * chars.length)];
    el.style.left = Math.random() * 100 + '%';
    el.style.fontSize = (2 + Math.random() * 3) + 'rem';
    el.style.animationDelay = (Math.random() * 2) + 's';
    document.body.appendChild(el);
    el.classList.add('rise');
    el.addEventListener('animationend', () => el.remove());
  }
}

// --- Main draw logic ---
let isDrawing = false;

async function startDraw() {
  if (isDrawing) return;
  isDrawing = true;

  const box = document.getElementById('omikujiBox');
  box.classList.add('shaking');

  // Fetch fortune while shaking
  const res = await fetch('/api/draw');
  const fortune = await res.json();

  // Shake for dramatic effect
  await sleep(1800);

  box.classList.remove('shaking');

  // Screen shake
  document.body.classList.add('screen-shake');
  setTimeout(() => document.body.classList.remove('screen-shake'), 500);

  // Flash
  const flash = document.getElementById('flash');
  flash.classList.add('flash');
  setTimeout(() => flash.classList.remove('flash'), 800);

  // Floating kanji
  spawnFloatingKanji();

  // Light beams
  triggerLightBeams(fortune.color);

  // Fireworks (center)
  const cx = window.innerWidth / 2;
  const cy = window.innerHeight / 2;
  spawnFirework(cx, cy, fortune.color, 80);
  setTimeout(() => spawnFirework(cx - 100, cy - 50, '#ffd700', 40), 200);
  setTimeout(() => spawnFirework(cx + 100, cy - 50, '#ffffff', 40), 400);

  // Extra fireworks for 大吉
  if (fortune.rank >= 6) {
    setTimeout(() => {
      spawnConfetti(120);
      spawnFirework(cx - 200, cy, '#ff44ff', 50);
      spawnFirework(cx + 200, cy, '#00ff88', 50);
    }, 600);
    setTimeout(() => spawnConfetti(80), 1200);
  }

  // Hide draw phase, show result
  await sleep(400);
  document.getElementById('drawPhase').style.display = 'none';

  const area = document.getElementById('resultArea');
  area.classList.add('visible');

  // Update result card accent color
  document.documentElement.style.setProperty('--accent', fortune.color);

  const card = document.getElementById('resultCard');
  card.style.borderColor = fortune.color;

  // Reveal card
  card.classList.add('reveal');

  await sleep(400);
  document.getElementById('resultEmoji').textContent = fortune.emoji;

  await sleep(300);
  const resultText = document.getElementById('resultText');
  resultText.textContent = fortune.result;
  resultText.classList.add('show');

  // Sparks on text reveal
  spawnSparks(cx, cy - 30, fortune.color, 30);

  await sleep(200);
  const sub = document.getElementById('resultSub');
  sub.textContent = '— ' + fortune.sub + ' —';
  sub.classList.add('show');

  await sleep(200);
  const msg = document.getElementById('resultMessage');
  msg.textContent = fortune.message;
  msg.classList.add('show');

  document.getElementById('retryBtn').classList.add('show');

  // Additional celebration for top fortunes
  if (fortune.rank >= 6) {
    setTimeout(() => spawnFloatingKanji(fortune.result), 1000);
    setTimeout(() => {
      spawnFirework(cx, cy - 100, fortune.color, 60);
      spawnConfetti(60);
    }, 1500);
  }

  isDrawing = false;
}

function resetDraw() {
  // Clean up
  particles = [];
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Reset result area
  const area = document.getElementById('resultArea');
  area.classList.remove('visible');
  const card = document.getElementById('resultCard');
  card.classList.remove('reveal');
  document.getElementById('resultText').classList.remove('show');
  document.getElementById('resultText').textContent = '';
  document.getElementById('resultSub').classList.remove('show');
  document.getElementById('resultSub').textContent = '';
  document.getElementById('resultMessage').classList.remove('show');
  document.getElementById('resultMessage').textContent = '';
  document.getElementById('resultEmoji').textContent = '';
  document.getElementById('retryBtn').classList.remove('show');

  // Show draw phase
  document.getElementById('drawPhase').style.display = '';
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
</script>
</body>
</html>"""
)


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
