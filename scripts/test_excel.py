import pandas as pd

file_path = r"C:\Users\RODRIGUE SINGOR\Desktop\mon site\site_projet_fin_etude\back-end\data\meteo_douala4.xlsx"

try:
    data = pd.read_excel(file_path, engine='xlrd')  # ou supprime engine pour laisser pandas choisir
    print(data.head())
except Exception as e:
    print("Erreur lors de la lecture du fichier :", e)
