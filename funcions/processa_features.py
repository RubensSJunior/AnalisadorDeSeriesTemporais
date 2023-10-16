import pandas as pd

from darts import TimeSeries
from sklearn.preprocessing import MinMaxScaler
from darts.dataprocessing.transformers import Scaler
from statsmodels.tsa.seasonal import seasonal_decompose 
from statsmodels.tsa.stattools import adfuller 
from scipy.stats import kendalltau
from darts.models import RandomForest

def preencheDataVazias(df,frequencia):
    df = df[["data","target"]]
    df["data"] = pd.to_datetime(df["data"],format='%Y-%m-%d')
    datas = pd.date_range(start=df["data"].min(), end=df["data"].max(), freq=frequencia)
    dfPreencher = df.set_index("data")
    completeTimeDf = pd.DataFrame()
    completeTimeDf["data"] = datas
    print(datas)
    completeTimeDf = completeTimeDf.set_index("data")
    completeTimeDf["target"] = dfPreencher["target"]
    
    return completeTimeDf.fillna(0)


def criaSerieTemporalDarts(df,epoch):
    margemPrevisao = round(len(df)/10)
    df_treino = df[:-margemPrevisao]
    df_teste = df[-margemPrevisao:]
    serieTreino = TimeSeries.from_dataframe(df_treino.reset_index(), 'data', 'target')
    serieTeste = TimeSeries.from_dataframe(df_teste.reset_index(), 'data', 'target')
    scalerMimMax = MinMaxScaler(feature_range=(1, 3))
    scaler = Scaler(scalerMimMax)
    serieTreinoScaled = scaler.fit_transform(serieTreino)
    serieTesteScaled = scaler.fit_transform(serieTeste)
    
    model = RandomForest(
    lags=12,
    output_chunk_length=12,
    n_estimators=epoch,
    criterion="absolute_error",
)
    
    model.fit(serieTreinoScaled)
    scaledPredictionSeries = model.predict(len(serieTesteScaled)+15)
    
    predictionSeries = scaler.inverse_transform(scaledPredictionSeries)
    dfPrediction = pd.DataFrame({'data': predictionSeries.time_index, 'target': list(predictionSeries.values())})
    dfPrediction["Previsao"] = dfPrediction["target"].apply(lambda x: x[0])

    
    dfPrediction = dfPrediction.set_index("data")
    dfPrediction["Real"] = df_teste["target"]
    
    
    return dfPrediction.fillna(0)


def decomposicaoSerieTemporal(df):
    serie = seasonal_decompose(df)
    trend_df = pd.DataFrame({'Trend': serie.trend})
    seasonal_df = pd.DataFrame({'Seasonal': serie.seasonal})
    residual_df = pd.DataFrame({'Residual': serie.resid})
    return trend_df, seasonal_df


def verificacaoEstacionaridade(data):
    result = adfuller(data, autolag='AIC')
    if result[1] < 0.05:
        return "Valor p = {}. Serie ja é estacionaria".format(round(result[1],5))
    else:
        return "Valor p = {}. Serie não é estacionaria".format(round(result[1],5))


def verificaTendencia(df):
    tau, p_value = kendalltau(x=df.index, y=df["target"].values)

    if p_value < 0.05:  # Você pode escolher um nível de significância adequado
        if tau > 0:
            return "Tendência positiva"
        elif tau < 0:
            return "Tendência negativa"
        else:
            return "Sem tendência significativa"
    else:
        return "Não há evidência suficiente para afirmar uma tendência significativa"