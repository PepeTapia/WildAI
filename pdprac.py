import numpy as np
import pandas as pd
import matplotlib.pylab as plt

df = pd.read_csv(r'A:\CodingProjects\WildAI\WildAI\Datasets\STM vs JDG Play-in\Game1.csv',index_col='Time')


s = pd.Series(np.random.randn(5))

print(s)

print(s+s)

print(s[0])
print(s[[1,4]])

new_df = df['team_gold'].diff()
df['gold diff'] = df['team_gold'].diff()
print(new_df)
df.plot(x='time', y='gold diff', kind='line')
plt.show()

new_df = df.loc[40]
gold_df = new_df.at[40,'team_gold']
print(type(gold_df))