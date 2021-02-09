# libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 
# Create a dataframe
value1=[7, 7, 5]
value2=[9, 6, 5]
value3 = [9, 6, 5]
df = pd.DataFrame({'group':['The 1st Method', 'The 2nd Method', 'The 3rd Method'], 'n = 10':value1 , 'n = 30':value2, 'n = 90': value3})
 
# Reorder it following the values of the first value:
ordered_df = df.sort_values(by='group')
my_range=range(1,len(df.index)+1)
 
# The vertical plot is made using the hline function
# I load the seaborn library only to benefit the nice looking feature
import seaborn as sns
plt.hlines(y=my_range, xmin=ordered_df['n = 10'], xmax=ordered_df['n = 90'], color='grey', alpha=1)
plt.scatter(ordered_df['n = 10'], my_range, color='#fa9802', alpha=1, label='n = 10')
plt.scatter(ordered_df['n = 30'], my_range, color='#0292a3', alpha=1 , label='n = 30')
plt.scatter(ordered_df['n = 90'], my_range, color='#06d822', alpha=1 , label='n = 90')
plt.legend()
 
# Add title and axis names
plt.yticks(my_range, ordered_df['group'])
plt.title("Comparison of the number of waitlist transplants for different numbers of incompatible pairs", loc='left')
plt.xlabel('Number of Waitlist Transplants')
plt.ylabel('Method')
plt.grid ()
plt.show ()