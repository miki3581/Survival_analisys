import numpy as np
import pandas as pd


def load_data():    

    # Load data, index_col=0 to set first column as index
    df = pd.read_csv('support2.csv', index_col=0)
    
    return df