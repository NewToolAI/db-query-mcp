import json
from pathlib import Path
from typing import Dict, Any
from elasticsearch import Elasticsearch

from db_query_mcp.db_adapters.base_adapter import BaseAdapter


class ElasticsearchDBAdapter(BaseAdapter):
    
    def __init__(self, db_uri: str, index: str, ca_certs: str = None, **kwargs):
        self.db_uri = db_uri
        self.index = index
        self.ca_certs = ca_certs

        if ca_certs:
            self.es = Elasticsearch(db_uri, ca_certs=ca_certs, **kwargs)
        else:
            self.es = Elasticsearch(db_uri, **kwargs)
            
        self._test_connection()

    def query(self, query: dict) -> str:
        response = self.es.search(index=self.index, body=query)

        response_dict = response.to_dict() if hasattr(response, 'to_dict') else dict(response)
        return json.dumps(response_dict, indent=2, ensure_ascii=False)

    def get_db_type(self) -> str:
        return 'elasticsearch'
    
    def get_db_schema(self) -> str:
        mapping = self.es.indices.get_mapping(index=self.index)
        settings = self.es.indices.get_settings(index=self.index)
        stats = self.es.indices.stats(index=self.index)
        
        schema_info = {
            'mapping': mapping.to_dict() if hasattr(mapping, 'to_dict') else dict(mapping),
        }

        return json.dumps(schema_info, indent=2, ensure_ascii=False)

    def export(self, query: dict, output: str) -> str:
        response = self.es.search(index=self.index, body=query)

        output_path = Path(output)
        if output_path.is_dir():
            export_file = output_path / 'export.json'
            if export_file.exists():
                raise FileExistsError(f'File {export_file.resolve()} already exists.')
        elif output_path.exists():
            raise FileExistsError(f'File {output_path} already exists.')
        else:
            export_file = output_path
            
        self._export_to_json(export_file, response)
            
        return f'Successfully exported data to {export_file.resolve()}'
    
    def _test_connection(self):
        if not self.es.ping():
            raise Exception('Cannot connect to Elasticsearch.')
            
        if not self.es.indices.exists(index=self.index):
            raise Exception(f'Index {self.index} does not exist.')
    
    def _export_to_json(self, output_path: Path, response: Dict[str, Any]):
        response_dict = response.to_dict() if hasattr(response, 'to_dict') else dict(response)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(response_dict, f, indent=2, ensure_ascii=False)
    