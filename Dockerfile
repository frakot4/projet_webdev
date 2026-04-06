# 1. Utiliser une image Python légère
FROM python:3.12-slim

# 2. Définir le dossier de travail
WORKDIR /app

# 3. Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier le fichier requirements et installer les lib Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier tout le reste du code
COPY . .

# 6. Variables d'environnement par défaut
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# 7. Collecter les fichiers statiques et lancer les migrations + le serveur
# Note : on ajuste le chemin vers manage.py car ton code est dans le sous-dossier projet_webdev
CMD python projet_webdev/manage.py collectstatic --noinput && \
    python projet_webdev/manage.py migrate && \
    gunicorn --bind 0.0.0.0:$PORT projet_webdev.wsgi
