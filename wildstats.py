import numpy as np
import pandas as pd
import matplotlib.pylab as plt

df = pd.read_csv(r'A:\CodingProjects\WildAI\WildAI\Datasets\NV vs FG Play-in\Game1.csv',index_col='time')
#print(df)
s = df['top_kill','top_gold']
#print(type(s))
print(s)
#print(type(s[298]))