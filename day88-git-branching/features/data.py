"""
Data module
"""

class DataManager:
    """Data manager"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.features = ["read", "write", "delete"]
    
    def get_version(self):
        return self.version
    
    def get_features(self):
        return self.features
