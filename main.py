from data_loader import load_data
from preprocess import clean_data


df = load_data()
df = clean_data(df)
print(df.head())