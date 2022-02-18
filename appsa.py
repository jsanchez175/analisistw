import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import preprocessor as p
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from PIL import Image
import re
import plotly.express as px
from user import df_tweet
from datetime import date
from datetime import datetime
import streamlit.components.v1 as components


#nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

#Removing stopwords
stop = nltk.corpus.stopwords.words('spanish')
plt.style.use('fivethirtyeight')

consumer_key = 'kIyGXKtu3tCDLhFhR8Ii3dLCe'
consumer_secret = 'ji5N35alH2bUb5kAlVKncXVLubuwWeS7Iwf4PuneyaGJu2N6l3'
access_token = '1392850256241610755-Mx8ftaRkyL9Gkc5AqMstoic6DKJOeQ'
access_token_secret = 'iwkjvXJi83oWbhmhp4BojCRoIyTkFloF5az8edPe5aUgW'

st.set_option('deprecation.showPyplotGlobalUse', False)
p.set_options(p.OPT.URL, p.OPT.RESERVED,p.OPT.NUMBER)

#Create the authentication object
authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
# Set the access token and access token secret
authenticate.set_access_token(access_token, access_token_secret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)

n = 100
    
def app():
    st.title("Analisis de cuentas en Twitter")
    st.header('Trabajo Final Febrero 2022')
    st.info("Proyecto impulsado por la Sociedad Ecuatoriana de Estadística")
    st.subheader("¿Qué cuenta quieres analizar?")
    raw_text = st.text_area("Ingresa la cuenta que deseas analizar (sin la @)")
    
    if st.button("Analizar"):
        texto = "Analizando los últimos " +  str(n) +" tweets de la cuenta"
        st.success(texto)
            hashtags = df['Tweets'].apply(lambda x: pd.value_counts(re.findall('(#\w+)', x.lower() )))\
                .sum(axis=0).to_frame().reset_index().sort_values(by=0,ascending=False)
            hashtags.columns = ['hashtag','occurences']
            fig = px.bar(hashtags, x='hashtag', y='occurences')
            st.plotly_chart(fig) 
        except:
            st.write("No tiene hashtags")
        
        
        st.subheader("Con quién interactua más la cuenta")
        
        try:
            usuarios = df['Tweets'].apply(lambda x: pd.value_counts(re.findall('(@\w+)', x.lower() )))\
            .sum(axis=0)\
            .to_frame()\
            .reset_index()\
            .sort_values(by=0,ascending=False)
            usuarios.columns = ["usuarios","interacciones"]
            usuarios["interacciones"] = usuarios["interacciones"].astype(int)
        
            col1, col2= st.columns(2)
            col1.metric(label="El total de personas con las que interactua ", value=usuarios.shape[0])
            col2.metric("Interacciones que tuve con mi mejor amigo en twitter", int(usuarios["interacciones"][:1].values))    
     
            html_str = f"""<br>No deja de conversar con <div style="color:red;font-size:35px;">{usuarios.iloc[0].iat[0]}</div>"""
            st.markdown(html_str, unsafe_allow_html=True)
        
            usuario = usuarios.iloc[0].iat[0]
            texto = "<a href=""https://twitter.com/" +usuario+ "?ref_src=twsrc%5Etfw"" class=""twitter-follow-button"" data-lang=""es"" data-show-count=""false"">Follow " +usuario+"</a><script async src=""https://platform.twitter.com/widgets.js"" charset=""utf-8""></script>"

            components.html(texto,height= 100)
            st.subheader("Mi top ten de conversaciones")
        
            st.table(usuarios.set_index("usuarios").head(10))
        
            #Actividad
            st.subheader("¿ Qué tan activa es la cuenta?")
            df.sort_values("mes",ascending=False, inplace=True)
            usuario = df.groupby("mes")["Tweets"].count()
            fig = px.line(usuario, x=usuario.index, y='Tweets')
            st.plotly_chart(fig)
        
            #Popularidad
            st.subheader("¿ Cuál fue el tweet con mas interacción ?")
            maximo = df["retweet_count"].max() 
            tweet_id = df[df["retweet_count"]==maximo].head(1)
            tweet_id = tweet_id["status_id"].values
            st.metric("Cantidad de RT's",int(maximo))
            result = api.get_oembed(int(tweet_id)) # , omit_script=True
            html = result['html'].strip()
            components.html(html,height= 1000)
        except:
            st.write("No tiene mayor interacción")
        
        
        st.caption("Powered by Jorge Sanchez bajo supervisión de Roberto Estevez")
        
if __name__ == "__main__":
	app()
