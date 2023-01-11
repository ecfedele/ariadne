# ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║ File:        CeaDatasetGenerator.py                                                                           ║
# ║ Namespace:   N/A                                                                                              ║
# ║ Project:     Ariadne/ModelBuilding                                                                            ║
# ║ Author:      Elijah Creed Fedele                                                                              ║
# ║ Date:        January 10, 2023                                                                                 ║
# ║ Description: Implements random (uniform) data input domain generation via Monte Carlo method and populates    ║
# ║              that data using the RocketCEA Python wrapper to the NASA Chemical Equilibrium with Applications  ║
# ║              combustion code.                                                                                 ║
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

import numpy  as np
import pandas as pd

## @class CeaDatasetGenerator
#  Encapsulates logic which generates an exemplary training dataset using Monte Carlo methods and a statistically
#  uniform source for input generation to CEA.
class CeaDatasetGenerator:
    fuel = ""
    oxidizer = ""
    elements = 0

    ## Constructor for a CeaDatasetGenerator object. Stores user selections for future invocation (i.e. when 
    #  self.get_cea_data() is called) and prepares the input domain.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param fuel      A string name of the chemical used as fuel in combustion. Passed directly to CEA.
    #  @param oxidizer  A string name of the chemical used as oxidizer in combustion. Passed directly to CEA.
    #  @param n         The number of elements to populate the input domain sample with.
    #
    #  @returns         None (constructor)
    def __init__(self, fuel, oxidizer, n=10000):
        self.fuel     = fuel
        self.oxidizer = oxidizer
        self.elements = n
        (self.pressure, self.mixture, self.area_ratio) = self.__get_domains__()

    ## Returns a Pandas DataFrame object consisting of the input domain selections.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #
    #  @returns         a DataFrame consisting of the input domain
    def get_input_dataframe(self):
        d = {'pressure': self.pressure, 'mixture': self.mixture, 'area_ratio': self.area_ratio}
        return pd.DataFrame(data=d)

    ## Generates the three principle Monte Carlo input lists based on minimum/maximum selections by the caller.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param p_min     The minimum pressure (rated in bar, 10^5 Pa) to consider within the dataset
    #  @param p_max     The maximum pressure (rated in bar, 10^5 Pa) to consider within the dataset 
    #  @param phi_min   The minimum mixture ratio (u/l) to consider within the dataset
    #  @param phi_max   The maximum mixture ratio (u/l) to consider within the dataset
    #  @param eps_min   The minimum area ratio (u/l) to consider within the dataset
    #  @param n         The size of the dataset to generate
    #
    #  @returns         a tuple of Numpy arrays consisting of the dataset dimensions
    def __get_domains__(self, p_min=2.5, p_max=750.0, phi_min=0.01, phi_max=50.0, eps_min=1.0, eps_max=200.0):
        pc  = np.random.default_rng().uniform(low=p_min, high=p_max, size=self.elements)
        phi = np.random.default_rng().uniform(low=phi_min, high=phi_max, size=self.elements)
        eps = np.random.default_rng().uniform(low=eps_min, high=eps_max, size=self.elements)
        return (pc, phi, eps)