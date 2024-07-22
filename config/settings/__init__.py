from __future__ import absolute_import, unicode_literals

# Import Celery app to ensure it's always loaded when Django starts
from ..celery import app as celery_app

__all__ = ('celery_app',)

# Existing imports (ensure these are also included)
from .base import *
from .development import *
