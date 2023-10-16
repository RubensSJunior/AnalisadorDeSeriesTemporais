import pandas as pd

def validaColunas(df):
    try:
        data = df["data"]
        target = df["target"]
        return True
    except:
        return False

def validaDataType(df):
    try:
        df["data"] = pd.to_datetime(df["data"],format='%Y-%m-%d')
        df["target"] = df["target"].apply(lambda x:float(x))
        return True
    except:
        return False
    
def validaQuantidadeDados(df):
    
    if len(df) > 100:
        return True
    else:
        return False
    
    