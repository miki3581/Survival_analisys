from data_loader import load_data
import pandas as pd
import numpy as np

def clean_data(df) -> pd.DataFrame:

    # Loading data
    df = load_data()

    # Dropping model, prediction, death related and summarising columns
    df.drop(columns=["aps", "sps", "surv2m", "surv6m", "prg2m", "prg6m", "dnr", "dnrday", "hospdead", "slos", "charges", "totcst", "totmcst"], inplace=True)

    # Mapping categorical variables to numerical values
    df["sex"] = df["sex"].map({"female": 0, "male": 1})
    df["income"] = df["income"].map({"under $11k": 0, "$11k-$25k": 1, "$25k-$50k": 2, ">$50k": 3})
    df["race"] = df["race"].map({"white": 0, "black": 1, "asian": 2, "other": 3, "hispanic": 4})
    df["ca"] = df["ca"].map({"no": 0, "yes": 1, "metastatic": 2})
    df["sfdm2"] = df["sfdm2"].map({"no(M2 and SIP pres)": 0, "adl>=4 (>=5 if sur)": 1, "SIP>=30": 2, "Coma or Intub": 3, "<2 mo. follow-up": 4})

    # Removing illneses other than ARF/MOSF
    remove = ["COPD/CHF/Cirrhosis", "Cancer", "Coma"]
    df = df.drop(df[df["dzclass"].isin(remove)].index)

    print(df.info())
    return df
    
