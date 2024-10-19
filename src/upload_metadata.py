import os
import json
from datetime import datetime, UTC
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from loguru import logger

def upload_metadata(directory, es_host='localhost', es_port=9200, es_username='elastic', es_password='changeme', index_name='metadata_index'):
    es = Elasticsearch(f"http://{es_host}:{es_port}", basic_auth=(es_username, es_password))

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    def generate_actions():
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    data['timestamp'] = datetime.now(UTC).isoformat()
                    yield {
                        '_index': index_name,
                        '_source': data
                    }
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from {filename}: {e}")
            except Exception as e:
                logger.error(f"Error reading file {filename}: {e}")

    try:
        success, failed = bulk(es, generate_actions())
        logger.info(f"Successfully uploaded {success} documents. Failed to upload {len(failed)} documents.")
    except Exception as e:
        logger.error(f"Error during bulk upload: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 -m src.upload_metadata <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    upload_metadata(directory)
