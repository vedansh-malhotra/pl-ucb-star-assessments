import prairielearn as pl
import pandas as pd
import numpy as np

def generate(data):
    df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                         "bar", "bar", "bar", "bar"],
                   "B": ["one", "one", "one", "two", "two",
                         "one", "one", "two", "two"],
                   "C": ["small", "large", "large", "small",
                         "small", "large", "small", "small",
                         "large"],
                   "D":["a","a","a","a","a","a","b","c","a"],
                   "E": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                   "F": [2, 4, 5, 5, 6, 6, 8, 9, 9],
                   "G": [2, 1, 5, 3, 6, 6, 7, 7, 9]})
    
    #Randomization process will go through at pl-pivot-table-random
    #This process is for simply providing fundamental of randomization
    #Randomization will be done by rotating elements in values and values of aggfunc dic
    '''table = pd.pivot_table(df, values=['E','F','G'], index=['A'],
        aggfunc={'E': "mean",
                 'F': ["min", "max", "mean"],
                 'G': np.median})'''

    data["params"]["orginal"] = pl.to_json(df.head(10))
