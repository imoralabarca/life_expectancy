from abc import ABC, abstractmethod
import pandas as pd

class DataStrategy(ABC):
    """Abstract strategy for loading and saving data."""

    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        pass

class CSVDataStrategy(DataStrategy):
    """Concrete strategy for CSV data handling."""
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)
    
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        df.to_csv(output_path, index=False)

class JSONDataStrategy(DataStrategy):
    """Concrete strategy for JSON data handling."""
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_json(file_path)
    
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        df.to_json(output_path, orient='records', lines=True)
