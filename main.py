from data_loader import load_data
from preprocess import clean_data, impute_data, scale_data


def main():

    df = load_data()
    df = clean_data(df)
    df = impute_data(df)
    df = scale_data(df)
    print(df.head())
    

if __name__ == "__main__":
    main()

