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

import re
import numpy             as     np
import pandas            as     pd
from   rocketcea.cea_obj import CEA_Obj

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
        self.fuel       = fuel
        self.oxidizer   = oxidizer
        self.elements   = n
        self.cea        = CEA_Obj(oxName=self.oxidizer, fuelName=self.fuel)
        (self.pressure, self.mixture, self.area_ratio) = self.__get_domains__()
        self.input_data = self.get_input_dataframe()

    ## Obtain CEA data for entire listed input domain (i.e. the dataframe contained in self.input_data).
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #
    #  @returns         A Pandas DataFrame consisting of the input domain plus CEA results
    def get_cea_data(self):
        pressure_throat     = []
        pressure_exit       = []
        molar_mass_chamber  = []
        molar_mass_throat   = []
        molar_mass_exit     = []
        adiabat_chamber     = []
        adiabat_throat      = []
        adiabat_exit        = []
        temperature_chamber = []
        temperature_throat  = []
        temperature_exit    = []
        rho_chamber         = []
        rho_throat          = []
        rho_exit            = []
        spec_heat_chamber   = []
        spec_heat_throat    = []
        spec_heat_exit      = []
        visc_chamber        = []
        visc_throat         = []
        visc_exit           = []
        cond_chamber        = []
        cond_throat         = []
        cond_exit           = []
        prandtl_chamber     = []
        prandtl_throat      = []
        prandtl_exit        = []
        
        for index, row in self.input_data.iterrows():
            cea_output = self.cea.get_full_cea_output(Pc=row['pressure'], 
                                                      MR=row['mixture'], 
                                                      eps=row['area_ratio'], 
                                                      short_output=1, 
                                                      show_transport=1, 
                                                      pc_units='bar')
            extraction_dict = self.__extract_properties__(cea_output)
            

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

    ## Pseudo-private method which uses regular expressions to extract relevant thermodynamic parameters from CEA 
    #  full output string.
    #  
    #  @param self       The reference to the calling CeaDatasetGenerator object
    #  @param cea_string The full output string received from CEA_Obj.get_full_cea_output()
    #
    #  @returns          A dictionary consisting of relevant parameters for use by self.get_cea_data()
    def __extract_properties__(self, cea_string):
        pressure_results    = re.search(r"P, ATM\s*\d+.\d+\s*(\d+.\d+)\s*(\d+.\d+)", cea_string)
        temperature_results = re.search(r"T, K\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+)", cea_string)
        molar_mass_results  = re.search(r"M, \(1/n\)\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+)", cea_string)
        adiabat_results     = re.search(r"GAMMAs\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+)", cea_string)
        pressure_throat     = float(pressure_results(1)) * 1.01325
        pressure_exit       = float(pressure_results(2)) * 1.01325
        molar_mass_chamber  = float(molar_mass_results(1))
        molar_mass_throat   = float(molar_mass_results(2))
        molar_mass_exit     = float(molar_mass_results(3))
        adiabat_chamber     = float(adiabat_results(1))
        adiabat_throat      = float(adiabat_results(2))
        adiabat_exit        = float(adiabat_results(3))
        temperature_chamber = float(temperature_results(1))
        temperature_throat  = float(temperature_results(2))
        temperature_exit    = float(temperature_results(3))
        return { "pressure_throat":     pressure_throat, 
                 "pressure_exit":       pressure_exit,
                 "molar_mass_chamber":  molar_mass_chamber,
                 "molar_mass_throat":   molar_mass_throat,
                 "molar_mass_exit":     molar_mass_exit,
                 "adiabat_chamber":     adiabat_chamber,
                 "adiabat_throat":      adiabat_throat,
                 "adiabat_exit":        adiabat_exit,
                 "temperature_chamber": temperature_chamber,
                 "temperature_throat":  temperature_throat,
                 "temperature_exit":    temperature_exit }