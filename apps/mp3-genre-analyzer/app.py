import os
import json
import tempfile
import logging

import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30MB

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

# ---------------------------------------------------------------------------
# モデル & ラベルの遅延ロード（Cold-start 時に1回だけ実行）
# ---------------------------------------------------------------------------
_embedding_model = None
_genre_model = None
GENRE_LABELS = []


def _load_models():
    global _embedding_model, _genre_model, GENRE_LABELS

    if _embedding_model is not None:
        return

    from essentia.standard import (
        TensorflowPredictEffnetDiscogs,
        TensorflowPredict2D,
    )

    logger.info("Loading Discogs-EffNet embedding model …")
    _embedding_model = TensorflowPredictEffnetDiscogs(
        graphFilename=os.path.join(MODEL_DIR, 'discogs-effnet-bs64-1.pb'),
        output='PartitionedCall:1',
    )

    logger.info("Loading genre_discogs400 classification head …")
    _genre_model = TensorflowPredict2D(
        graphFilename=os.path.join(
            MODEL_DIR, 'genre_discogs400-discogs-effnet-1.pb'
        ),
        input='serving_default_model_Placeholder',
        output='PartitionedCall:0',
    )

    label_path = os.path.join(
        MODEL_DIR, 'genre_discogs400-discogs-effnet-1.json'
    )
    with open(label_path, 'r') as f:
        metadata = json.load(f)
    GENRE_LABELS.extend(metadata.get('classes', []))
    logger.info("Models loaded – %d genre labels", len(GENRE_LABELS))


# ---------------------------------------------------------------------------
# ジャンル解析
# ---------------------------------------------------------------------------
def analyze_genre(filepath):
    """MP3 ファイルを解析し、上位5ジャンルを返す。"""
    _load_models()

    from essentia.standard import MonoLoader

    audio = MonoLoader(
        filename=filepath, sampleRate=16000, resampleQuality=4
    )()

    embeddings = _embedding_model(audio)
    predictions = _genre_model(embeddings)

    # フレームごとの予測を平均
    avg = np.mean(predictions, axis=0)

    top_idx = np.argsort(avg)[::-1][:5]
    results = []
    for idx in top_idx:
        raw = GENRE_LABELS[idx]
        # "Rock---Alternative Rock" → parent="Rock", sub="Alternative Rock"
        if '---' in raw:
            parent, sub = raw.split('---', 1)
        else:
            parent, sub = raw, raw
        results.append({
            'genre': sub,
            'parent': parent,
            'confidence': round(float(avg[idx]) * 100, 1),
        })
    return results


# ---------------------------------------------------------------------------
# ルーティング
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルが選択されていません'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400

    if not file.filename.lower().endswith('.mp3'):
        return jsonify({'error': 'MP3ファイルのみ対応しています'}), 400

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
        file.save(tmp.name)
        try:
            results = analyze_genre(tmp.name)
            return jsonify({'results': results})
        except Exception as e:
            logger.exception("Analysis failed")
            return jsonify({'error': f'解析中にエラーが発生しました: {e}'}), 500
        finally:
            os.unlink(tmp.name)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    app.run(host='0.0.0.0', port=port)
