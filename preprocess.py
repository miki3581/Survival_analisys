import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler


def clean_data(df) -> pd.DataFrame:

    # Dropping model, prediction, death related and summarising columns
    to_drop = ["aps", "sps", "surv2m", "surv6m", "prg2m", "prg6m", "dnr", "dnrday", "hospdead", "slos", "charges", "totcst", "totmcst", "ca", "sfdm2", "avtisst"]
    df.drop(columns = to_drop, inplace = True)

    # Dropping rows with missing targets
    df.dropna(subset=["d.time", "death"], inplace=True)
    df = df[df["d.time"] > 0]

    # Mapping categorical variables to numerical values
    df["sex"] = df["sex"].map({"female": 0, "male": 1})

    # One hot encoding race
    one_hot = pd.get_dummies(df["race"], prefix = "race")
    df = pd.concat([df, one_hot], axis = 1)
    df.drop(columns = ["race"], inplace = True)

    # Removing illneses other than colon cancer
    remove = ["ARF/MOSF w/Sepsis", "CHF", "COPD", "Lung Cancer", "MOSF w/Malig", "Coma", "Cirrhosis"]
    df = df.drop(df[df["dzgroup"].isin(remove)].index)
    df.drop(columns = ["dzgroup", "dzclass"], inplace = True)

    # Dropping columns with >50% nulls
    to_drop2 = ["income", "ph", "glucose"]
    df.drop(columns = to_drop2, inplace = True)
    
    # Imputing missing data with normal fill-in values provided by 
    values = {
        "alb": 3.5,
        "pafi": 333.3,
        "bili": 1.01,
        "crea": 1.01,
        "bun": 6.51,
        "wblc": 9,
        "urine": 2502
    }
    df.fillna(value = values, inplace = True)

    return df

def impute_data(df) -> pd.DataFrame:

    # Imputing other variables using KNN
    imputer = KNNImputer(n_neighbors=5)
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns = df.columns, index = df.index)

    return df_imputed

def scale_data(df) -> pd.DataFrame:
    
    # Scaling data
    scaler = StandardScaler()
    
    cols_to_exclude = ["d.time", "death", "sex"] + [col for col in df.columns if "race" in col]
    cols_to_scale = [col for col in df.columns if col not in cols_to_exclude]
    
    df_scaled = df.copy()
    df_scaled[cols_to_scale] = scaler.fit_transform(df_scaled[cols_to_scale])
    
    return df_scaled
