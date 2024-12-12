from loguru import logger

from elasticsearch import Elasticsearch
from datetime import datetime
from apps.core.settings import settings

import sys

es_host = settings.ELASTICSEARCH_HOST
es_port = settings.ELASTICSEARCH_PORT
es_login_url = f'http://{es_host}:{es_port}'
# Initialize Elasticsearch client
es = Elasticsearch(hosts=[es_login_url])


# Configure loguru to push logs to Elasticsearch
def log_to_elasticsearch(message):
    try:
        log_record = message.record
        log_data = {
            "@timestamp": datetime.utcnow().isoformat(),
            "level": log_record["level"].name,
            "message": log_record["message"],
            "module": log_record["module"],
            "function": log_record["function"],
            "line": log_record["line"],
        }
        es.index(index="logger_index", document=log_data)
    except Exception as e:
        logger.error(f"Failed to log to Elasticsearch: {e}")


# Configure loguru
logger.remove()  # Remove default logger
logger.add(sys.stdout, level="INFO")  # Console logging
logger.add(log_to_elasticsearch, level="INFO")  # Elasticsearch logging
