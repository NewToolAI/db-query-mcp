from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    
    @abstractmethod
    def query(self, query: str) -> str:
        pass

    @abstractmethod
    def export(self, query: str, csv_path: str) -> str:
        pass

    @abstractmethod
    def get_db_type(self) -> dict:
        pass
    
    @abstractmethod
    def get_db_schema(self) -> str:
        pass
