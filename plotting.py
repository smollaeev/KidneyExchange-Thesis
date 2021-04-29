# libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 
# Create a dataframe
value1=[7, 7, 7]
value2=[7, 7, 5]
value3 = [7, 7, 7]
df = pd.DataFrame({'group':['The 1st Scenario', 'The 2nd Scenario', 'The 3rd Scenario'], 'p = 20':value1 , 'p = 40':value2, 'p = 60': value3})
 
# Reorder it following the values of the first value:
ordered_df = df.sort_values(by='group')
my_range=range(1,len(df.index)+1)
 
# The vertical plot is made using the hline function
# I load the seaborn library only to benefit the nice looking feature
import seaborn as sns
plt.hlines(y=my_range, xmin=ordered_df['p = 20'], xmax=ordered_df['p = 60'], color='grey', alpha=1)
plt.scatter(ordered_df['p = 20'], my_range, color='#fa9802', alpha=1, label='p = 20')
plt.scatter(ordered_df['p = 40'], my_range, color='#0292a3', alpha=1 , label='p = 40')
plt.scatter(ordered_df['p = 60'], my_range, color='#06d822', alpha=1 , label='p = 60')
plt.legend()
 
# Add title and axis names
plt.yticks(my_range, ordered_df['group'])
plt.title("Comparison of the number of waiting list transplants for different numbers of population size", loc='left')
plt.xlabel('Number of Waiting List Transplants')
plt.ylabel('Scenario')
plt.grid ()
plt.show ()