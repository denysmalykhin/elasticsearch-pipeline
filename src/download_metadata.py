import json
from datetime import datetime
from elasticsearch import Elasticsearch
from loguru import logger

def download_metadata(start_date, end_date, directory, es_host='localhost', es_port=9200, es_username='elastic', es_password='changeme', index_name='metadata_index'):
    es = Elasticsearch(f"http://{es_host}:{es_port}", basic_auth=(es_username, es_password))

    query = {
            "range": {
                "timestamp": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        }

    try:
        result = es.search(index=index_name, query=query, scroll='2m', size=100)
        scroll_id = result['_scroll_id']
        hits = result['hits']['hits']
        if len(hits) == 0:
            logger.error(f"No hits found for the period {start_date} to {end_date}")
        else:
            while len(hits) > 0:
                for hit in hits:
                    filename = f"{directory}/download_{hit['_id']}.json"
                    with open(filename, 'w') as f:
                        json.dump(hit['_source'], f, indent=2)
                
                result = es.scroll(scroll_id=scroll_id, scroll='2m')
                scroll_id = result['_scroll_id']
                hits = result['hits']['hits']
                print(result)

            logger.info(f"Downloaded metadata files for the period {start_date} to {end_date}")
    except Exception as e:
        logger.error(f"Error during download: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Usage: python download_metadata.py <start_date> <end_date> <directory>")
        print("Date format: YYYY-MM-DD")
        sys.exit(1)
    
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    directory = sys.argv[3]
    download_metadata(start_date, end_date, directory)
