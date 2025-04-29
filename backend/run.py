# backend/run.py
import os
from app import create_app

# Determinar entorno desde variable de entorno o usar default
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Determinar puerto desde variable de entorno o usar default (5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)