# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 19:25:26 2020

@author: gogliom
"""

######

# CERCO UNA LISTA DI POSSIBILI MODI CON CUI CHIAMARE PREZZO MATERIA PRIMA
# PROVO A RECUPERARE PREZZO MATERIA PRIMA
# CREO UN CARTESIANO E CALCOLO DISTANZA TRA OGNI POSSIBILE COPPIA NOME-PREZZO
# PRENDO VALORE CON DISTANZA MINORE 

#Doc = "D:\Altro\RPA\Energy\IREN\TEST CTE\CTE\esempi cte\Energit-Casa-Web.pdf"

import pandas as pd
import re
import numpy as np

def PrezzoComponenteEnergia(Doc):
    
    PossiblePrice = []
    Base = []
    
    
    #Doc = convert_pdf_to_txt(Doc)
    #Doc = Doc.upper()
    
    #le inserisco come regular expression perchè non so quanti spazi ci sono e se magari c'è una new line (\s+)
    r1 = 'CORRISPETTIVO\s+LUCE\s+'
    r2 = 'COMPONENTE\s+PREZZO\s+ENERGIA'
    r3 = 'PREZZO\s+LUCE'
    r4 = 'PREZZO.+COMPONENTE.+ENERGIA'
    r5 = 'COMPONENTE\s+ENERGIA'
    r6 = 'MONORARI'
    r7 = 'MONORARIO'
    r8 = 'F0'
    r9 = 'PREZZO.{0,10}ENERGIA'

    regex = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    
    regex = re.compile('|'.join(regex))
    
    
    Base = [m.start() for m in regex.finditer(Doc)]
    Base = pd.DataFrame(Base, columns = ['PositionBase'])
    
    
    
    #prendo i numeri positivi  
    #regexNum1 = r'-?\d*\,.?\d+'
    #regexNum2 = r'-?\d*\..?\d+'
    
    regexNum1 = r'\d+\,?\d+'
    regexNum2 = r'\d+\.?\d+'
    
    
    regexNum = [regexNum1, regexNum2]
    
    regexNum = re.compile('|'.join(regexNum))
    
    
    NumberPos = [m.start() for m in regexNum.finditer(Doc)]
    NumberValue = regexNum.findall(Doc)
    NumberTuples = list(zip(NumberValue,NumberPos))
    
    
    PossiblePrice = pd.DataFrame(NumberTuples, columns=['Price', 'Position'])
    #converto in numero
    PossiblePrice['Price_NUM'] = PossiblePrice.apply(lambda row: row.Price.replace(",","."), axis = 1)
    PossiblePrice['Price_NUM'] = PossiblePrice.apply(lambda row: row.Price_NUM.replace(" ",""), axis = 1)
    PossiblePrice['Price_NUM'] = PossiblePrice.apply(lambda row: float(row.Price_NUM), axis = 1)
    
    #filtro numeri < 1 e positivi
    PossiblePrice = PossiblePrice[(PossiblePrice['Price_NUM'] > 0.02) & (PossiblePrice['Price_NUM'] < 0.1)]
    
    '''
    APPROCCIO IN BASE AL QUALE CERCO €/KWH E PRENDO PAROLA PRECEDENTE, MA IN ALCUNI CASI NELLE TABELLE NON E ESPLICITATA
    EURO/KWH VICINO AL NUMERO
    ii = 0
    for ww in Doc.split():
        if "€/KWH" in ww or "EURO/KWH" in ww:
            pw = Doc.split()[ii-1]
            po = Doc.find(Doc.split()[ii-1]+" "+Doc.split()[ii])
            nn = pd.DataFrame({'Price': [pw], 'Position': [po]})
            PossiblePrice = PossiblePrice.append(nn) 
            #Positions = Positions + list(ii-1)        
        ii = ii + 1 
    #estraggo i numeri 
    PossiblePrice['Price'] = PossiblePrice.apply(lambda row: re.findall('-?\d*\,.?\d+', str(row.Price)), axis=1)
    #elimino eventuali stringe vuote
    PossiblePrice = PossiblePrice[PossiblePrice['Price'].apply(lambda row: len(row)) > 0]
    '''
    
    
    
    Base['key'] = 0
    PossiblePrice['key'] = 0
    
    Prezzo = Base.merge(PossiblePrice, how='outer')
    Prezzo['dist'] = Prezzo.apply(lambda row: row.Position - row.PositionBase, axis = 1)
    #FILTRO PER LE DISTANZE POSITIVE (IL NUMERO VIENE DOPO LA PAROLA, OPPURE NEGATIVE MOLTO PICCOLE DOVE QUINDI LA BASE VIENE IMMEDIATAMENTE DOPO )
    Prezzo = Prezzo[Prezzo['dist'] > - 25]
    
    
    Prezzo = Prezzo.nsmallest(1, 'dist')
    
    
    # VERIFICO VARIABILITA' PREZZO     
    v1 = r'\bPUN\b'
    v2 = r'^(?=.*\bPREZZO\b)(?=.*\bUNICO\b)(?=.*\bNAZIONALE\b).*$'
    v3 = r'^(?=.*\bINGROSSO\b)(?=.*\bBORSA\b)(?=.*\bELETTRICA\b).*$'
    v4 = r'^(?=.*\bFORMULA\b)(?=.*\bPREZZO\b)(?=.*\bENERGIA\b).*$'
    v5 = r'PREZZO.{0,10}ENERGIA.{0,30}TIV'
    
    regexVar = [v1, v2, v3, v4, v5]
    
    regexVar = re.compile('|'.join(regexVar))
    
    PriceExplanation= []
    PriceExplanation = [m.start() for m in regexVar.finditer(Doc)]
    '''
    for i in Doc.split('\n'):
        if regexVar.match(i):
            PriceExplanation.append(i)
    '''
    #  VERIFICO SE SI PARLA DI COME VIENE CALCOLATO IL PREZZO DELLA COMPONENTE ENERGIA
    
    f1 = r'PREZZ.{1,30}ENERGIA.{1,50}FISS'
    f2 = r'PREZZ.{1,30}ENERGIA.{1,50}INVARIABIL'

    regexFix = [f1, f2]
    
    regexFix = re.compile('|'.join(regexFix))
    
    PriceFix= []
    PriceFix = [m.start() for m in regexFix.finditer(Doc)]
    

    
    if len(PriceExplanation) == 0 or len(PriceFix) > 0:
        Prezzo['TipoPrezzo'] = 'Fisso'
    else:
        Prezzo['TipoPrezzo'] = 'Variabile'
        if pd.isnull(Prezzo['Price']).any():
            Prezzo['Price'].values = 'Variabile'

    return (Prezzo['Price'], Prezzo['TipoPrezzo'])
    
   

    ########APPROCCIO FRANCESCO
def VerificaVariabilitàPrezzo(Doc):
    
    v1 = r'\bPUN\b'
    v2 = r'^(?=.*\bPREZZO\b)(?=.*\bUNICO\b)(?=.*\bNAZIONALE\b).*$'
    v3 = r'^(?=.*\bINGROSSO\b)(?=.*\bBORSA\b)(?=.*\bELETTRICA\b).*$'
    v4=  r'^(?=.*\bFORMULA\b)(?=.*\bPREZZO\b)(?=.*\bENERGIA\b).*$'
    
    regexVar = [v1, v2, v3,v4]
    
    regexVar = re.compile('|'.join(regexVar))
    regexVar  


    PriceExplanation= []
    for i in Doc.split('\n'):
        if regexVar.match(i):
            PriceExplanation.append(i)
 
    return PriceExplanation