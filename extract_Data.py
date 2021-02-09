import pandas as pd
dataFrame = pd.read_json ('DonorData.json')
dataFrame.to_csv ('DonorData.csv', index = False)
