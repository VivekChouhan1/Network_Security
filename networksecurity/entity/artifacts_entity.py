## This store the output of DataIngestion

from dataclasses import dataclass
## act as decoretor and create variable for empty class


@dataclass
class DataIngestionArtifacts:
    train_file_path:str
    test_file_path:str


