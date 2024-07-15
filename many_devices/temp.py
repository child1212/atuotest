#%%

from queue import Queue
from time import sleep
q = Queue(maxsize=0)
q.put(0)
q.put(1)
q.put(2)
for i in range(3):
    print(q.get())
    print(q.queue)

# %%
