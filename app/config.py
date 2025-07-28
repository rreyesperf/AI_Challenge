import os

class Config:
    DEBUG = False
    APP_INSIGHTS_INSTRUMENTATION_KEY = os.environ.get('APP_INSIGHTS_INSTRUMENTATION_KEY')
    # Other configuration settings...
