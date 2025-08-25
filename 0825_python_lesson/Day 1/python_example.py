import pandas as pd

def clean_data(df):
    """Cleans the dataframe by removing rows with missing values and dropping unnecessary columns."""
    df = df.dropna()
    df = df.drop(columns=['gender', 'ip_address'])
    return df

if __name__ == '__main__':
    df = pd.read_csv('data.csv')
    df_clean = clean_data(df)
    df_clean.to_csv('clean_data.csv', index=False)
