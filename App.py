# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 15:28:47 2021

@author: gogliom
"""


import streamlit as st
from PIL import Image
from ElabFile import ElabFile 
from Read_Pdf import read_pdf  #importazione basata sul pacchetto che tiene struttura
from LetturaPdf_2 import read_pdf_2 #importaizone basata sulla convert_pdf_to_txt e poi splittata in ele / gas in base ai paragrafi
from ProvePerNomeOfferta import Name

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
image = Image.open('MicrosoftTeams-image.png')
st.sidebar.image(image, width=225)



st.sidebar.subheader("Seleziona la commodity")
add_selectbox = st.sidebar.selectbox('',
    ('Energia', 'Gas'))

st.sidebar.subheader("Carica un file")
uploaded_file = st.sidebar.file_uploader("")

st.markdown("<h1 style='text-align: center; color: black;'>CTE Extractor</h1>", unsafe_allow_html=True)






if uploaded_file is not None:
    #la lettura del file può avvenire una volta sola
    #quindi dalla read pdf mi porto fuori anche il pdf con struttura che servità ad es per la name
        try:  #in un caso la lettura della convert_pdf_to_txt va in errore -> in except metto lettura con struttura
            Read = read_pdf(uploaded_file)
        except:
            Read = read_pdf_2(uploaded_file)
            
        Commodity = Read[0]
        Energia = Read[1]
        Gas = Read[2] 
        PdfSt = Read[3]
        
    
        #carico cmq tutto il documento con la struttura anche per usarlo in alternativa 
        try:
            Read2 = read_pdf_2(uploaded_file)
            
            Energia2 = Read2[1]
            Gas2 = Read2[2] 
        except:
            Energia2 = Energia
            Gas2 = Gas 
            
            
        Res = ElabFile(Commodity, Energia, Energia2, Gas, Gas2, PdfSt)

        
        st.write(Res)

    
    
  