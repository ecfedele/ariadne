# ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║ File:        CeaDatasetGeneratorTest2.py                                                                      ║
# ║ Namespace:   N/A                                                                                              ║
# ║ Project:     Ariadne/ModelBuilding                                                                            ║
# ║ Author:      Elijah Creed Fedele                                                                              ║
# ║ Date:        January 11, 2023                                                                                 ║
# ║ Description: Small unit test file which tests the CeaDatasetGenerator class functionality after CEA data      ║
# ║              bindings have been added.                                                                        ║
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

# Figure generation options for publication - instruct Matplotlib to generate 1200 DPI figures with labels in the 
# Computer Modern Roman (serif) font.
plt.rcParams.update({
    "text.usetex"        : True,
    "text.latex.preamble": [r"\usepackage{amsmath}", r"\usepackage{amssymb}"],
    "font.family"        : "serif",
    "font.serif"         : ["Computer Modern Serif"],
    "figure.dpi"         : 1200,
    "savefig.dpi"        : 1200
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

# Construct a 4x4 histogram plot using Matplotlib. Save the file to a figure.
fig, axs = plt.subplots(4, 4)
axs[0, 0].hist(df.loc[:, 'pressure_throat'],     bins=50, density=True, alpha=0.6, color='b', ec='black')
axs[0, 0].set_title(r"Throat pressure ($p_t$) (bar abs.)")
axs[0, 0].set_xlabel("Pressure (bar)")
axs[0, 1].hist(df.loc[:, 'pressure_exit'],       bins=50, density=True, alpha=0.6, color='g', ec='black')
axs[0, 1].set_title(r"Nozzle exit pressure ($p_e$) (bar abs.)")
axs[0, 1].set_xlabel("Pressure (bar)")
axs[0, 2].hist(df.loc[:, 'molar_mass_chamber'],  bins=50, density=True, alpha=0.6, color='r', ec='black')
axs[0, 2].set_title(r"Chamber exhaust molar mass ($\mathfrak{M}_c$) (kg/kmol)")
axs[0, 2].set_xlabel(r"Molar mass (kg/kmol)")
axs[0, 3].hist(df.loc[:, 'molar_mass_throat'],   bins=50, density=True, alpha=0.6, color='c', ec='black')
axs[0, 3].set_title(r"Throat exhaust molar mass ($\mathfrak{M}_t$) (kg/kmol)")
axs[0, 3].set_xlabel(r"Molar mass (kg/kmol)")
axs[1, 0].hist(df.loc[:, 'molar_mass_exit'],     bins=50, density=True, alpha=0.6, color='m', ec='black')
axs[1, 0].set_title(r"Nozzle exit exhaust molar mass ($\mathfrak{M}_e$) (kg/kmol)")
axs[1, 0].set_xlabel(r"Molar mass (kg/kmol)")
axs[1, 1].hist(df.loc[:, 'adiabat_chamber'],     bins=50, density=True, alpha=0.6, color='y', ec='black')
axs[1, 1].set_title(r"Chamber adiabatic index ($\gamma_c$)")
axs[1, 1].set_xlabel("Adiabatic index")
axs[1, 2].hist(df.loc[:, 'adiabat_throat'],      bins=50, density=True, alpha=0.6, color='b', ec='black')
axs[1, 2].set_title(r"Chamber adiabatic index ($\gamma_t$)")
axs[1, 2].set_xlabel("Adiabatic index")
axs[1, 3].hist(df.loc[:, 'adiabat_exit'],        bins=50, density=True, alpha=0.6, color='g', ec='black')
axs[1, 3].set_title(r"Chamber adiabatic index ($\gamma_e$)")
axs[1, 3].set_xlabel("Adiabatic index")
axs[2, 0].hist(df.loc[:, 'temperature_chamber'], bins=50, density=True, alpha=0.6, color='r', ec='black')
axs[2, 0].set_title(r"Chamber temperature ($T_c$) (K)")
axs[2, 0].set_xlabel("Temperature (K)")
axs[2, 1].hist(df.loc[:, 'temperature_throat'],  bins=50, density=True, alpha=0.6, color='c', ec='black')
axs[2, 1].set_title(r"Throat temperature ($T_t$) (K)")
axs[2, 1].set_xlabel("Temperature (K)")
axs[2, 2].hist(df.loc[:, 'temperature_exit'],    bins=50, density=True, alpha=0.6, color='m', ec='black')
axs[2, 2].set_title(r"Nozzle exit temperature ($T_e$) (K)")
axs[2, 2].set_xlabel("Temperature (K)")
axs[2, 3].hist(df.loc[:, 'rho_chamber'],         bins=50, density=True, alpha=0.6, color='y', ec='black')
axs[2, 3].set_title(r"Chamber gas density ($\rho_c$) (kg/m$^3$)")
axs[2, 3].set_xlabel(r"Gas density (kg/m$^3$)")
axs[3, 0].hist(df.loc[:, 'rho_throat'],          bins=50, density=True, alpha=0.6, color='b', ec='black')
axs[3, 0].set_title(r"Throat gas density ($\rho_t$) (kg/m$^3$)")
axs[3, 0].set_xlabel(r"Gas density (kg/m$^3$)")
axs[3, 1].hist(df.loc[:, 'rho_exit'],            bins=50, density=True, alpha=0.6, color='g', ec='black')
axs[3, 1].set_title(r"Nozzle exhaust gas density ($\rho_e$) (kg/m$^3$)")
axs[3, 1].set_xlabel(r"Gas density (kg/m$^3$)")
axs[3, 2].hist(df.loc[:, 'spec_heat_chamber'],   bins=50, density=True, alpha=0.6, color='r', ec='black')
axs[3, 2].set_title(r"Chamber specific heat ($c_{pc}$) (kJ/kg$\cdot$K)")
axs[3, 2].set_xlabel(r"Specific heat (kJ/kg$\cdot$K)")
axs[3, 3].hist(df.loc[:, 'spec_heat_throat'],    bins=50, density=True, alpha=0.6, color='c', ec='black')
axs[3, 3].set_title(r"Throat specific heat ($c_{pc}$) (kJ/kg$\cdot$K)")
axs[3, 3].set_xlabel(r"Specific heat (kJ/kg$\cdot$K)")
for ax in axs.flat:
    ax.set_ylabel("Frequency")
plt.savefig('TestingOutputs/Histogram.png')