import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../modules')
import pandas as pd
import numpy as np
import DataFrameUtil as myDf
import GraphiqueUtile as myGraph
import matplotlib.pyplot as plt
import seaborn as sns
import inspect
import datetime

months = ["", "janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "aout", "sept.", "oct.", "nov.", "déc."]

def getMonthAndYear(moisStr):
    year = np.nan
    month = np.nan
    if moisStr != None:
        ss = moisStr.strip().split()
        if len(ss) > 1 :
            year = int(ss[len(ss)-1])
        m = ss[0]
        month = months.index(m)
    return month, year


def cleanType(df, verbose=False):
    frame = inspect.currentframe()
    functionName = inspect.getframeinfo(frame).function
    print("Function", functionName)

    # Convertir les types en numérique
    # Remplacer les virgules par des points pour que la conversion en float soit possible
    df = df.apply(lambda x: x.str.replace(',','.'))
    colums = df.columns
    for col in colums:
        if col != "Mois":
            df[col] = pd.to_numeric(df[col])

    # Traiter les dates, convertir le format texte dans un format exploitable
    df["DATE"] = pd.to_datetime('today')
    for i in df.index:
        month, year = getMonthAndYear(df.loc[i, "Mois"])
        date = datetime.date(year=year, month=month, day=1)
        df.loc[i, "DATE"] = date
    df["DATE"] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
    if verbose:
        print(df[["Mois", "DATE"]])
        print(df.dtypes)

    print("Function", functionName, "......................................END")
    return df


def prepareData(df, verbose=False):
    frame = inspect.currentframe()
    functionName = inspect.getframeinfo(frame).function
    print("Function", functionName)
    df = cleanType(df, verbose)
    if verbose:
        myDf.displayMissingValues(df, verbose)
    df = myDf.cleanDuplicatedData(df=df, idColumnName="DATE", verbose=verbose, removeNbNanCol=False)

    # Suppression des lignes où il manque trop de données :
    if verbose:
        print("df.shape, BEFORE remove:", df.shape)
        dfTemp = df[df["NB_NAN"] == 6]
        print("6", dfTemp.shape)
        dfTemp = df[df["NB_NAN"] == 7]
        print("7", dfTemp.shape)
    dfRemove = df[df["NB_NAN"] < 6]
    if verbose: print("df.shape, AFTER remove:", dfRemove.shape)
    df = dfRemove
    print(functionName, " ........................................................ END")
    return df


verbose = False

print("Chargement des données....", end='')
# Climat des affaires en France
df = pd.read_csv('OC_4525336_ClimatAffaireFranceDATA.csv', sep=';')
print("......................................END")

verbose = True
# Préparation des données -------------------------------------------------------------------------
df = prepareData(df, verbose)

if verbose:
    myDf.displayInfo(df)
    print(df["NB_NAN"])
    print(df.describe())
    print("*************************************")

    dfTemp = df[df["NB_NAN"] == 4]
    print("4", dfTemp.shape)
    dfTemp = df[df["NB_NAN"] == 5]
    print("5", dfTemp.shape)



print(df.corr(method='spearman'))
print(df.corr(method='kendall'))
myGraph.showCorrelationSeaborn(df)


print("END")
