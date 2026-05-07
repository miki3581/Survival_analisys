from data_loader import load_data
from preprocess import clean_data, impute_data, scale_data, save_csv


def main():

    df = load_data()
    df_clean = clean_data(df)
    df_imputed = impute_data(df_clean)
    df_scaled = scale_data(df_imputed)
    print(df_scaled.head())
    save_csv(df_scaled)
    

if __name__ == "__main__":
    main()
