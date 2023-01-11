# ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║ File:        CeaDatasetGeneratorTest.py                                                                       ║
# ║ Namespace:   N/A                                                                                              ║
# ║ Project:     Ariadne/ModelBuilding                                                                            ║
# ║ Author:      Elijah Creed Fedele                                                                              ║
# ║ Date:        January 10, 2023                                                                                 ║
# ║ Description: Small unit test file which tests the input domain generation of CeaDatasetGenerator and performs ║
# ║              exemplary plotting of the data generated.
# ╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
# ║ Copyright (C) 2023 Elijah Creed Fedele                                                                        ║
# ║                                                                                                               ║
# ║ This program is free software: you can redistribute it and/or modify it under the terms of the GNU General    ║
# ║ Public License as published by the Free Software Foundation, either version 3 of the License, or (at your     ║
# ║ option) any later version.                                                                                    ║
# ║                                                                                                               ║
# ║ This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the    ║
# ║ implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License  ║
# ║ for more details.                                                                                             ║
# ║                                                                                                               ║
# ║ You should have received a copy of the GNU General Public License along with this program.  If not, see       ║
# ║ <http://www.gnu.org/licenses/>.                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

import matplotlib.cm       as cm
import matplotlib.pyplot   as plt
import numpy               as np
from   scipy.stats         import norm
from   CeaDatasetGenerator import CeaDatasetGenerator

# Figure generation options for publication - instruct Matplotlib to generate 600 DPI figures with labels in the 
# Computer Modern Roman (serif) font.
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif" : ["Computer Modern Serif"],
    "figure.dpi" : 600,
    "savefig.dpi": 600
})

# Generate the exemplary dataset using the CeaDatasetGenerator class. Use a smaller sample size for visualization 
# purposes. Print the resulting DataFrame to the console for verification.
cea = CeaDatasetGenerator("CH4", "LOX", n=1000)
df  = cea.get_input_dataframe()
print(df)

# Scan out the DataFrame to individual parameters to make plotting less obtuse. Construct an additional dimension, 
# 'w', as the Euclidean norm of the three input domain dimensions. Use this to construct an HSV colormap for the 
# scatterplot.
x = df.loc[:, "pressure"]
y = df.loc[:, "mixture"]
z = df.loc[:, "area_ratio"]
w = np.sqrt(np.square(x) + np.square(y) + np.square(z))
colors = cm.hsv(w / max(w))

# Plot 1: Form a scatterplot of the data and display it to the user.
fig = plt.figure(1)
ax = fig.add_subplot(projection='3d')
ax.scatter(x, y, z, c=colors, s=5)
ax.set_xlabel('Pressure (bar)')
ax.set_ylabel('Mixture ratio')
ax.set_zlabel('Area ratio')
plt.show()

# Run statistical tests on the individual data distributions 'x', 'y' and 'z' and display norm-fits w/ histogram 
# to the user.
mux, stdx = norm.fit(x)
muy, stdy = norm.fit(y)
muz, stdz = norm.fit(z)

plt.figure(2)
plt.grid()
plt.hist(x, bins=50, density=True, alpha=0.6, color='r', ec='black')
mux_str  = "{:.2f}".format(mux)
stdx_str = "{:.2f}".format(stdx)
plt.ylabel("Frequency")
plt.xlabel("Pressure (bar)")
plt.title(fr"$\mu$ = {mux_str} bar, $\sigma$ = $\pm${stdx_str} bar")

plt.figure(3)
plt.grid()
plt.hist(y, bins=50, density=True, alpha=0.6, color='g', ec='black')
muy_str  = "{:.2f}".format(muy)
stdy_str = "{:.2f}".format(stdy)
plt.ylabel("Frequency")
plt.xlabel("Mixture ratio")
plt.title(fr"$\mu$ = {muy_str}, $\sigma$ = $\pm${stdy_str}")

plt.figure(4)
plt.grid()
plt.hist(z, bins=50, density=True, alpha=0.6, color='b', ec='black')
muz_str  = "{:.2f}".format(muz)
stdz_str = "{:.2f}".format(stdz)
plt.ylabel("Frequency")
plt.xlabel("Area ratio")
plt.title(fr"$\mu$ = {muz_str}, $\sigma$ = $\pm${stdz_str}")
