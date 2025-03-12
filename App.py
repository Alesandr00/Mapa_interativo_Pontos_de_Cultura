import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

df = pd.read_csv("pontosdecultura-redeculturaviva.csv", encoding="latin1", delimiter=";")

df[["Latitude","Longitude"]] = df["Localização"].str.split(",", expand=True)
df["Latitude"] = df["Latitude"].astype(float)
df["Longitude"] = df["Longitude"].astype(float)

df_cleaned = df.dropna(subset=['Latitude', 'Longitude', 'Nome', 'Nome Entidade/Coletivo Cultural', 'Estado', 'Município', 'Endereço', 'Ações Estruturantes',
                               'Públicos que participam das ações', 'Área de experiência e temas', 'Atuação', 'Email Público', 'Telefone Público', 'Site',
                               'Instagram', 'Youtube'])

st.title("🌍 Mapa Interativo de Pontos de Cultura")
st.write("Explore os espaços culturais e suas informações detalhadas.")

estado_opcoes = df_cleaned["Estado"].unique().tolist()
estado_selecionado = st.selectbox("Filtrar por Estado:", ["Todos"] + estado_opcoes)

if estado_selecionado != "Todos":
    df_filtrado = df_cleaned[df_cleaned["Estado"] == estado_selecionado]
else:
    df_filtrado = df_cleaned

latitude_media = df_filtrado["Latitude"].mean()
longitude_media = df_filtrado["Longitude"].mean()
mapa = folium.Map(location=[latitude_media, longitude_media], zoom_start=5)

for _, row in df_filtrado.iterrows():
    popup_texto = f"""
        <div style="width: 250px; font-family: Arial, sans-serif; font-size: 14px; padding: 10px; border-radius: 10px; background-color: #f9f9f9; border: 1px solid #ddd; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #333; text-align: center;">{row['Nome']}</h4>
            <p><b>Nome Entidade:</b> {row['Nome Entidade/Coletivo Cultural']}</p>
            <p><b>Estado:</b> {row['Estado']}</p>
            <p><b>Município:</b> {row['Município']}</p>
            <p><b>Endereço:</b> {row['Endereço']}</p>
            <p><b>Ações Estruturantes:</b> {row['Ações Estruturantes']}</p>
            <p><b>Área de experiência:</b> {row['Área de experiência e temas']}</p>
            <p><b>Atuação:</b> {row['Atuação']}</p>
            <p><b>Email:</b> <a href='mailto:{row['Email Público']}'>{row['Email Público']}</a></p>
            <p><b>Telefone:</b> {row['Telefone Público']}</p>
            <p><b>Site:</b> <a href='{row['Site']}' target='_blank'>{row['Site']}</a></p>
            <p><b>Instagram:</b> <a href='{row['Instagram']}' target='_blank'>{row['Instagram']}</a></p>
            <p><b>Youtube:</b> <a href='{row['Youtube']}' target='_blank'>{row['Youtube']}</a></p>
        </div>
    """
    
    iframe = folium.IFrame(html=popup_texto, width=300, height=300)
    folium.Marker([row["Latitude"], row["Longitude"]], popup=folium.Popup(iframe)).add_to(mapa)
  
folium_static(mapa)
