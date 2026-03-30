# Add these settings to your existing healix/settings.py
# ─────────────────────────────────────────────────────────

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── INSTALLED APPS (add to existing list) ──
HEALIX_APPS = [
    'patients',   # already exists
    'api',        # new
    'corsheaders',
]

# ── TEMPLATES: add landing + dashboard dirs ──
# In your TEMPLATES setting, add to DIRS:
# BASE_DIR / 'templates'

# ── STATIC FILES ──
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_URL = '/static/'

# ── AI CONFIGURATION ──
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
HEALIX_LLM_MODEL = os.getenv('HEALIX_LLM_MODEL', 'gpt-4o-mini')

# ── MONGODB (via djongo) ──
# Replace default DATABASES with:
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': os.getenv('MONGO_DB_NAME', 'healix'),
#         'CLIENT': {
#             'host': os.getenv('MONGO_URI', 'mongodb://localhost:27017'),
#         }
#     }
# }

# ── CORS (for Next.js frontend if used) ──
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_ALL_ORIGINS = os.getenv('DEBUG', 'True') == 'True'

# ── MIDDLEWARE: add corsheaders ──
# Add 'corsheaders.middleware.CorsMiddleware' BEFORE CommonMiddleware

# ── LOGGING ──
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'healix': {
            'format': '[{levelname}] {asctime} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'healix',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'ai_engine': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# SECURITY FIX: Store API keys in environment variables
# Example: api_key = os.getenv('API_KEY')
