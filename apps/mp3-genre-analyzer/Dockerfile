FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libfftw3-3 \
    libyaml-0-2 \
    libsamplerate0 \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Essentia pre-trained models (Discogs-EffNet + genre_discogs400)
RUN mkdir -p models && \
    wget -q -O models/discogs-effnet-bs64-1.pb \
      https://essentia.upf.edu/models/music-style-classification/discogs-effnet/discogs-effnet-bs64-1.pb && \
    wget -q -O models/genre_discogs400-discogs-effnet-1.pb \
      https://essentia.upf.edu/models/classification-heads/genre_discogs400/genre_discogs400-discogs-effnet-1.pb && \
    wget -q -O models/genre_discogs400-discogs-effnet-1.json \
      https://essentia.upf.edu/models/classification-heads/genre_discogs400/genre_discogs400-discogs-effnet-1.json

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "--timeout", "120", "--workers", "1", "app:app"]
