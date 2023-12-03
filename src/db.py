import json
from typing import Dict, List
from datetime import datetime

class JsonDB:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> Dict[str, List[Dict]]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write(self, data: Dict[str, List[Dict]]):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def insert(self, email: Dict):
        data = self.read()

        if "date" in email:            
            date_str = email['date']
            if date_str not in data:
                data[date_str] = []
            data[date_str].append(email)
            
        self.write(data)
        
    def count_objects(self) -> Dict[str, int]:
        data = self.read()
        
        return {key: len(value) for key, value in data.items()}
