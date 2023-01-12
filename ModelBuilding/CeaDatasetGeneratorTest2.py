# ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║ File:        CeaDatasetGeneratorTest2.py                                                                      ║
# ║ Namespace:   N/A                                                                                              ║
# ║ Project:     Ariadne/ModelBuilding                                                                            ║
# ║ Author:      Elijah Creed Fedele                                                                              ║
# ║ Date:        January 11, 2023                                                                                 ║
# ║ Description: Small unit test file which tests the CeaDatasetGenerator class functionality after CEA data      ║
# ║              bindings have been added.
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
import pandas              as pd
import time
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

# Generate the exemplary dataset using the CeaDatasetGenerator class. Use a large dataset to test the class under
# production conditions. Print the dataset to the user and export it under TestingOutputs/. Benchmark the function
# to see how long it takes under real conditions.
elements = 50000
start    = time.perf_counter()
cea      = CeaDatasetGenerator("CH4", "LOX", n=elements)
df       = cea.get_cea_data()
finish   = time.perf_counter()
duration = finish - start
print(f"Computed {elements} CEA elements in {duration} seconds ({float(elements) / duration} elements/s).")
print(df)
df.to_csv('TestingOutputs/CH4_LOX.csv', index=False)