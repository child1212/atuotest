#%%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

with open("device.txt","r") as f:
    for line in f:
        a = pd.read_csv(line.replace("\n", ""))
        c = a.drop_duplicates(["time"])
        b = np.array(c)
        plt.plot(b[:,0], b[:,1],"s-")
        plt.ylabel("FPS")
        plt.xlabel("time")
        plt.show()

# %%
