import streamlit as st
from funcions.valida_timeserie import validaColunas,validaDataType,validaQuantidadeDados
from funcions.processa_features import preencheDataVazias,decomposicaoSerieTemporal,verificacaoEstacionaridade,verificaTendencia,criaSerieTemporalDarts
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose



epoch = st.slider('Quantas Epocasvoce quer treinar', 1, 300, 200)
freq = st.selectbox(    'Sua serie é Mensal iniciando no começo do mes (MS), Mensal iniciando no final do mes (M)  ou Diaria (D)',('MS','M' , 'D',))


uploaded_file = st.file_uploader("Adicione o seu arquivo CSV com a serie temporal", accept_multiple_files=False)

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    
    if validaColunas(dataframe) == False:
        st.warning("alerta nome Colunas", icon="⚠️")
        
    if validaDataType(dataframe) == False:
        st.warning("alerta tipo colunas", icon="⚠️")
        
    if validaQuantidadeDados(dataframe) == False:
        st.warning("alerta tipo colunas", icon="⚠️")
    
    if validaColunas(dataframe) and validaDataType(dataframe) and validaQuantidadeDados(dataframe):
        if st.button('Get Product'):
            try :

                dfcompleto = preencheDataVazias(dataframe,freq)    
                dfcompleto_re = dfcompleto.reset_index()
                fig = px.line(dfcompleto_re, x="data", y="target")
                st.title('Serie Temporal Completa')
                
                fig.update_layout( autosize=False, width=1500, height=600, margin=dict( l=20, r=20, b=25, t=25, pad=4 ) ,
                                legend=dict( orientation="h", yanchor="bottom",  y=1.01, xanchor="right", x=0.8))
                st.plotly_chart(fig, use_container_width=True)

                tendencia,sazonalidade, = decomposicaoSerieTemporal(dfcompleto)
                
                tendeciaEncontrada = verificaTendencia(dfcompleto)
                st.header('Grafico de tendencia')
                st.subheader(tendeciaEncontrada)
                fig_t = px.line(tendencia.reset_index(), x="data", y="Trend")
                fig_t.update_layout( autosize=False, width=1500, height=600, margin=dict( l=20, r=20, b=25, t=25, pad=4 ) ,
                                legend=dict( orientation="h", yanchor="bottom",  y=1.01, xanchor="right", x=0.8))
                st.plotly_chart(fig_t, use_container_width=True)
                
                resultadoADF = verificacaoEstacionaridade(dfcompleto)
                st.header('Grafico de sazionalidade')
                st.subheader(resultadoADF)
                fig_s = px.line(sazonalidade.reset_index()[-20:], x="data", y="Seasonal")
                fig_s.update_layout( autosize=False, width=1500, height=600, margin=dict( l=20, r=20, b=25, t=25, pad=4 ) ,
                                legend=dict( orientation="h", yanchor="bottom",  y=1.01, xanchor="right", x=0.8))
                st.plotly_chart(fig_s, use_container_width=True)

                st.header('Previsão para os proximos 15 periodos')
                previsao = criaSerieTemporalDarts(dfcompleto,epoch)


                fig_p = px.line(previsao.reset_index(), x="data", y=["Previsao","Real"])
                fig_p.update_traces(line=dict(color="green"), selector=dict(name="Previsao"))
                fig_p.update_traces(line=dict(color="orange"), selector=dict(name="Real"))
                fig_p.update_layout( autosize=False, width=1500, height=600, margin=dict( l=20, r=20, b=25, t=25, pad=4 ) ,
                                legend=dict( orientation="h", yanchor="bottom",  y=1.01, xanchor="right", x=0.8))
                st.plotly_chart(fig_p, use_container_width=True)
                

            except Exception as error:
                # handle the exception

                st.warning("An exception occurred:{}".format(error), icon="⚠️")       

