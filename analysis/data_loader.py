import pandas as pd
from pathlib import Path

SRC_DIR = Path(__file__).parent
BASE_DIR = SRC_DIR.parent

def load_data(filename: str, sep: str = ",", decimal: str = ",", skiprows = [1]) -> pd.DataFrame:
    path = BASE_DIR / filename
    df = pd.read_csv(path, sep=sep, decimal=decimal, skiprows=skiprows)
    return df.drop(columns=["Komentarze"], errors="ignore")

def base_dir():
    return BASE_DIR

if __name__ == "__main__":
    df = load_data("data/pom-425.csv")
    print(f"pkt4: {df.shape} wczytane.")