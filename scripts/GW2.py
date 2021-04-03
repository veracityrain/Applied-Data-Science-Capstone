
import requests
import pandas as pd
from pandas import json_normalize


url_items = 'http://api.gw2tp.com/1/bulk/items.json'
url_itemname = 'http://api.gw2tp.com/1/bulk/items-names.json'

resp = requests.get(url=url_items)
data_items = resp.json() # Check the JSON Response Content documentation below

resp = requests.get(url=url_itemname)
data_itemname = resp.json() # Check the JSON Response Content documentation below

item_columns = data_items['columns']
item_rows = data_items['items']

itemname_columns = ['id','ItemName']
itemname_rows = data_itemname['items']

df_item = pd.DataFrame(data=item_rows,columns=item_columns)
df_itemname = pd.DataFrame(data=itemname_rows,columns=itemname_columns)

df_TP = df_itemname.join(df_item,lsuffix='_caller', rsuffix='_other')

df_TP.drop(columns=['id_caller','id_other'],inplace=True)
df_TP['FullStackBuy'] = df_TP['buy']*250
df_TP['FullStackSell'] = df_TP['sell']*250

df_Leg = df_TP.loc[df_TP['ItemName'].isin(['The Bifrost','Bolt','The Dreamer','The Flameseeker Prophecies',
'Frenzy','Frostfang','Howler','Incinerator','The Juggernaut','Kudzu','Kraitkin',"Kamohoali'i Kotaki",'Meteorlogicus', 'The Minstrel',
'The Moot','The Predator','Quip','Rodgort','Sunrise','Twilight','Eternity'])]

df_Prec = df_TP.loc[df_TP['ItemName'].isin(['The Legend','Zap','The Lover','The Chosen','Rage','Tooth of Frostfang',
'Howl','Spark','The Colossus','Leaf of Kudzu','Venom','Carcharias','Storm','The Bard','The Energizer',
'The Hunter','Chaos Gun',"Rodgort's Flame",'Dawn','Dusk'])]

df_T6 = df_TP.loc[df_TP['ItemName'].isin(['Vicious Fang','Armored Scale','Vicious Claw','Ancient Bone',
'Vial of Powerful Blood','Powerful Venom Sac','Elaborate Totem','Pile of Crystalline Dust'])]

df_GiftOfMetal = df_TP.loc[df_TP['ItemName'].isin(['Orichalcum Ingot','Mithril Ingot','Platinum Ingot','Darksteel Ingot'])]


df_Summary = pd.DataFrame(columns=['Grouped Items','BuyPrice','SellPrice'],
data=[
['T6',df_T6['FullStackBuy'].sum(),df_T6['FullStackSell'].sum()],
['Ecto',df_TP.loc[df_TP['ItemName'] == 'Glob of Ectoplasm']['FullStackBuy'].sum(),df_TP.loc[df_TP['ItemName'] == 'Glob of Ectoplasm']['FullStackSell'].sum()],
['Icy Runestone',1000000,1000000],
['Gift of Metal',df_GiftOfMetal['FullStackBuy'].sum(),df_GiftOfMetal['FullStackSell'].sum()],
['Gift of Wood','','']
])

print(df_Summary)
print(df_Leg)
print(df_Prec)
