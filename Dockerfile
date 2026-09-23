# 1. Utiliser une image Python légère
FROM python:3.12-slim

# 2. Définir le dossier de travail
WORKDIR /app

# 3. Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier le fichier requirements et installer les lib Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier tout le reste du code dans /app
COPY . .

# 6. Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH=/app/projet_webdev

# Changement de dossier : On se place explicitement là où se trouve la vraie base de données
WORKDIR /app/projet_webdev

# 7. Collecter les fichiers statiques, migrer et lancer Gunicorn (plus besoin de préciser les chemins)
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    gunicorn --bind 0.0.0.0:$PORT projet_webdev.wsgi
