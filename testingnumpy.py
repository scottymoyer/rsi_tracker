import numpy as np

x = np.array([[[1,2],[3,4],[5,6]],[[10,2],[3,4],[5,6]],[[1,2],[3,4],[5,6]],[[100,2],[3,4],[5,6]]])

for i in x[::-1]:
  print(i)

y = x[::-1]
print(y)