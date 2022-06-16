import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

colorList = ['black', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'gold', 'orange', 'seagreen', 'cornflowerblue', 'midnightblue', 'olivedrab', 'chocolate', 'linen', 'lightcoral', 'azure', 'turquoise', 'darkorange', 'bisque', 'forestgreen', 'slategrey', 'crimson', 'lawngreen', 'lightgoldenrodyellow', 'fuchsia', 'mediumaquamarine', 'burlywood', 'lavender', 'wheat', 'greenyellow', 'peru', 'teal', 'indigo', 'rebeccapurple', 'mediumpurple', 'snow', 'darkgreen', 'oldlace']
cmap = colors.ListedColormap(colorList, name="Colors", N=None)
dimList = [-0.5]
for i in range(len(colorList)):
	dimList.append(i-0.5)

def displayMap(district_matrix):
	plt.imshow(district_matrix)
	plt.show()
	
def displayMapWithKnownColors(district_matrix):
	plt.imshow(district_matrix, cmap=cmap)
	plt.show()