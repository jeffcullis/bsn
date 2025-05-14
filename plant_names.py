import os
import re
import requests
import json

class PlantNames:

    UNIPROT_URL = "https://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/complete/docs/speclist.txt"
    DEFAULT_UNIPROT_FILE = "./data/uniprot_speclist.txt"
    DEFAULT_COMMON_KEYS_FILE = "./data/common_keys.json"

    def __init__(self, uniprot_file=None, common_keys_file=None):
        self.uniprot_file = uniprot_file or self.DEFAULT_UNIPROT_FILE
        self.common_keys_file = common_keys_file or self.DEFAULT_COMMON_KEYS_FILE
        self._common_names = {}
        if os.path.exists(self.common_keys_file):
            self._common_names = json.load(open(self.common_keys_file, 'r'))
        else:
            if not os.path.exists(self.uniprot_file):
                self._download_uniprot_file()
            self._load_uniprot_speclist()
            json.dump(self._common_names, open(self.common_keys_file, 'w'), indent=4)

    def _download_uniprot_file(self):
        if not os.path.exists(self.uniprot_file):
            response = requests.get(self.UNIPROT_URL)
            if response.status_code == 200:
                with open(self.uniprot_file, "wb") as file:
                    file.write(response.content)
                print(f"File downloaded successfully to {self.uniprot_file}")
            else:
                raise ValueError(f"Failed to download file. HTTP status code: {response.status_code}")

    def _load_uniprot_speclist(self):
        n_pattern = r".*N=(.*)"
        c_pattern = r".*C=(.*)"
        with open(self.uniprot_file, 'r') as file:
            n_found = False
            n_value = ''
            for line in file:
                if line.startswith('#') or not line.strip():
                    continue
                n_match = re.search(n_pattern, line)
                if n_match:
                    n_value = n_match.group(1).strip()
                    self._common_names[n_value] = None
                    n_found = True
                c_match = re.search(c_pattern, line)
                if c_match:
                    c_value = c_match.group(1).strip()
                    if not n_found:
                        raise ValueError(f"N= value not found before C= value in line: {line}")
                    self._common_names[n_value] = c_value
                    n_found = False                       

    def get_common_name(self, scientific_name):
        if self._common_names.get(scientific_name):
            return self._common_names[scientific_name]
        else:
            return ''
