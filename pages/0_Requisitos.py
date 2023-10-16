import streamlit as st 


st.markdown('''
            # Requisitos para utilização!
            ## A utilização dessa ferramenta necessita de aalguns requisitos basicos
            
            - O campo de data deve ser estar no formato YYYY-MM-DD e deve ter o nome 'data'
            - O campo do valor deve estar setado como um valor numerico e deve ter o nome 'target'
            
            ### A indicação de tipo de serie temporal segue o seguinte padrão
            - MS - Se sua serie temporal é mensal com valores no inicio do mes EX:1997-01-01    
            - M - Se sua serie temporal é mensal com valores no final do mes EX:1997-01-31
            - M - Se sua serie temporal é diaria 
            
            ### É necessario ter cuidado com a quantidade de epocas do treinamento, pois uma maior quantidades de epocas apesar de gerar um valor mais acurado pode demandar muito tempo execuçã.
            
            
            ''')
