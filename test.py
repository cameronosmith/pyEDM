import pandas as pd
import pyEDM
import numpy as np

df = pd.read_csv("twospike_data.csv")

# showt that prediction is good (contains non-1 values)

exclusion_matrix = np.zeros((df.shape[0],df.shape[0]))

for idx in range(70,83):
    exclusion_matrix[idx-1, -1+np.array(list(range(20,30)))] = 1

'''simplex_out = pyEDM.Simplex(dataFrame=df, E=3, tau=1, knn=20,
                        exclusionMatrix=pd.DataFrame( exclusion_matrix ),
                        lib="1 50", pred="71 81", columns="wave")
print(simplex_out)
'''

simplex_out = pyEDM.SMap(dataFrame=df, E=3, tau=1, knn=20,
                        exclusionMatrix=pd.DataFrame( exclusion_matrix ),
                        lib="1 50", pred="71 81", columns="wave")
print(simplex_out)



# construct exlcusion matrix( exclude all non-1 values)
