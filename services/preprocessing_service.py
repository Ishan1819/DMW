import pandas as pd

def handle_missing_values(df: pd.DataFrame):
    return df.fillna(df.mean(numeric_only=True))

def encode_categorical(df: pd.DataFrame):
    cat_cols = df.select_dtypes(include=['object']).columns
    return pd.get_dummies(df, columns=cat_cols, drop_first=True)

def remove_outliers(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
    return df
