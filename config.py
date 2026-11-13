import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'travel-planner-dev-key'