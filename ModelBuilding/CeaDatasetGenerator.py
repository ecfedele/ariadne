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

class CeaDatasetGenerator:
    fuel = ""
    oxidizer = ""
    elements = 0

    ## Constructor for a CeaDatasetGenerator object. Stores user selections for future invocation (i.e. when 
    #  self.get_cea_data() is called) and prepares data domain information for use in Monte Carlo generation.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param fuel      A string name of the chemical used as fuel in combustion. Passed directly to CEA.
    #  @param oxidizer  A string name of the chemical used as oxidizer in combustion. Passed directly to CEA.
    #  @param p_min     An optional parameter which specifies the lower limit of pressure (in bar, 10^5 Pa)
    #  @param p_max     An optional parameter which specifies the upper limit of pressure (in bar, 10^5 Pa)
    #  @param phi_min   An optional parameter which specifies the lower limit of propellant mixture ratio
    #  @param phi_max   An optional parameter which specifies the upper limit of propellant mixture ratio
    #  @param eps_min   An optional parameter which specifies the lower limit of nozzle expansion area ratio
    #  @param eps_max   An optional parameter which specifies the upper limit of nozzle expansion area ratio
    #  @param n         An optional parameter indicating the desired sample size.
    #
    #  @returns         None (constructor)
    def __init__(self, fuel, oxidizer, p_min=2.5, p_max=750.0, phi_min=0.01, phi_max=50.0, eps_min=1.0, 
                 eps_max=200.0, n=10000):
        self.fuel       = fuel
        self.oxidizer   = oxidizer
        self.elements   = n
        self.p_range    = [ p_min, p_max ]
        self.phi_range  = [ phi_min, phi_max ]
        self.eps_range  = [ eps_min, eps_max ]
        self.cea        = CEA_Obj(oxName=self.oxidizer, fuelName=self.fuel)
        col_names       = [ "fuel", "oxidizer", "pressure", "mixture", "area_ratio", "pressure_throat", 
                            "pressure_exit", "molar_mass_chamber", "molar_mass_throat", "molar_mass_exit", 
                            "adiabat_chamber", "adiabat_throat", "adiabat_exit", "temperature_chamber", 
                            "temperature_throat", "temperature_exit", "rho_chamber", "rho_throat", "rho_exit", 
                            "spec_heat_chamber", "spec_heat_throat", "spec_heat_exit", "visc_chamber", 
                            "visc_throat", "visc_exit", "cond_chamber", "cond_throat", "cond_exit", 
                            "prandtl_chamber", "prandtl_throat", "prandtl_exit", "mach_exit" ]
        self.data       = pd.DataFrame(columns=col_names)

    ## Fills out the self.data DataFrame to a size of self.elements with CEA data.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #
    #  @returns         The DataFrame constructed (self.data)
    def get_cea_data(self):
        while len(self.data.index) < self.elements:
            pressure   = np.random.default_rng().uniform(low=self.p_range[0],   high=self.p_range[1])
            mixture    = np.random.default_rng().uniform(low=self.phi_range[0], high=self.phi_range[1])
            area_ratio = np.random.default_rng().uniform(low=self.eps_range[0], high=self.eps_range[1])
            cea_fostr  = self.cea.get_full_cea_output(Pc=pressure, 
                                                      MR=mixture, 
                                                      eps=area_ratio, 
                                                      short_output=1, 
                                                      show_transport=1,
                                                      output='siunits',
                                                      pc_units='bar')
            if self.is_valid_cea_result(cea_fostr):
                (pressure_throat, pressure_exit) = self.get_pressures(cea_fostr)
                (molar_mass_chamber, molar_mass_throat, molar_mass_exit) = self.get_molar_masses(cea_fostr)
                (adiabat_chamber, adiabat_throat, adiabat_exit) = self.get_adiabat(cea_fostr)
                (temperature_chamber, temperature_throat, temperature_exit) = self.get_temperatures(cea_fostr)
                (rho_chamber, rho_throat, rho_exit) = self.cea.get_Densities(
                                                          Pc=(pressure * 14.5038),
                                                          MR=mixture,
                                                          eps=area_ratio 
                                                      )
                mach_exit = self.cea.get_MachNumber(Pc=(pressure * 14.5038), MR=mixture, eps=area_ratio)
                (spec_heat_chamber, visc_chamber, cond_chamber, prandtl_chamber) = self.cea.get_Chamber_Transport(
                                                                                       Pc=(pressure * 14.5038),
                                                                                       MR=mixture,
                                                                                       eps=area_ratio 
                                                                                   )
                (spec_heat_throat, visc_throat, cond_throat, prandtl_throat) = self.cea.get_Throat_Transport(
                                                                                   Pc=(pressure * 14.5038),
                                                                                   MR=mixture,
                                                                                   eps=area_ratio 
                                                                               )
                (spec_heat_exit, visc_exit, cond_exit, prandtl_exit) = self.cea.get_Exit_Transport(
                                                                           Pc=(pressure * 14.5038),
                                                                           MR=mixture,
                                                                           eps=area_ratio 
                                                                       )
                self.data.loc[len(self.data.index)] = [ self.fuel, self.oxidizer, pressure, mixture, area_ratio,
                                                        pressure_throat, pressure_exit, molar_mass_chamber, 
                                                        molar_mass_throat, molar_mass_exit, adiabat_chamber, 
                                                        adiabat_throat, adiabat_exit, temperature_chamber, 
                                                        temperature_throat, temperature_exit, rho_chamber, 
                                                        rho_throat, rho_exit, spec_heat_chamber, spec_heat_throat, 
                                                        spec_heat_exit, visc_chamber, visc_throat, visc_exit, 
                                                        cond_chamber, cond_throat, cond_exit, prandtl_chamber, 
                                                        prandtl_throat, prandtl_exit, mach_exit ]
        return self.data

    ## Gets input domain from internal DataFrame. Primarily used in an older version of CeaDatasetGenerator;
    #  incorporated to avoid breaking old unit tests.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #
    #  @returns         A DataFrame consisting of the input domain data
    def get_input_dataframe(self):
        if (len(self.data.index) == 0) or (len(self.data.index) is None):
            df = self.get_cea_data()
        d = { "pressure":   self.data.loc[:, 'pressure'],
              "mixture":    self.data.loc[:, 'mixture'],
              "area_ratio": self.data.loc[:, 'area_ratio'] }
        return pd.DataFrame(data=d)

    ## Checks, using regular expressions, if the CEA result is valid. Receives a full output string ('cea_fostr') 
    #  and scans for the term 'EXIT' (signifying all three standard engine stations were successfully computed) and
    #  the word 'NaN', which indicates a computational error resulting in an invalid floating-point value. Presence
    #  of the first ('EXIT') and absence of the second ('NaN') indicates a passed test. Failure to pass is a fail.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param cea_fostr The CEA full output string corresponding to the test conditions
    #
    #  @returns         A Boolean value indicating whether the result is valid or not
    def is_valid_cea_result(self, cea_fostr):
        exit_regexp = re.search(r"EXIT", cea_fostr)
        nan_regexp  = re.search(r"NaN",  cea_fostr)
        if (exit_regexp is not None) and (nan_regexp is None):
            return True
        else:
            return False

    ## Uses grouping regular expressions to extract the standard station pressures from the CEA full output.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param cea_fostr The CEA full output string corresponding to the test conditions
    #
    #  @returns         A tuple consisting of the pressure at the engine throat and the pressure at nozzle exit
    def get_pressures(self, cea_fostr):
        pressure_results = re.search(r"P, BAR\s*\d+.\d+\s*(\d+.\d+)\s*(\d+.\d+)", cea_fostr)
        pressure_throat  = float(pressure_results(1))
        pressure_exit    = float(pressure_results(2))
        return (pressure_throat, pressure_exit)

    ## Uses grouping regular expressions to extract the standard station molar masses from the CEA full output.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param cea_fostr The CEA full output string corresponding to the test conditions
    #
    #  @returns         A tuple consisting of the molar masses of the exhaust stream at the three standard engine 
    #                   stations
    def get_molar_masses(self, cea_fostr):
        molar_mass_results = re.search(r"M, \(1/n\)\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+)", cea_fostr)
        molar_mass_chamber = float(molar_mass_results(1))
        molar_mass_throat  = float(molar_mass_results(2))
        molar_mass_exit    = float(molar_mass_results(3))
        return (molar_mass_chamber, molar_mass_throat, molar_mass_exit)

    ## Uses grouping regular expressions to extract the standard station adiabatic indexes (ratios of specific 
    #  heat) from the CEA full output.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param cea_fostr The CEA full output string corresponding to the test conditions
    #
    #  @returns         A tuple consisting of the adiabatic indexes (ratios of specific heat) at the three standard
    #                   engine stations
    def get_adiabat(self, cea_fostr):
        adiabat_results = re.search(r"GAMMAs\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+)", cea_fostr)
        adiabat_chamber = float(adiabat_results(1))
        adiabat_throat  = float(adiabat_results(2))
        adiabat_exit    = float(adiabat_results(3))
        return (adiabat_chamber, adiabat_throat, adiabat_exit)

    ## Uses grouping regular expressions to extract the standard station temperature values from the CEA full 
    #  output.
    #
    #  @param self      The reference to the calling CeaDatasetGenerator object
    #  @param cea_fostr The CEA full output string corresponding to the test conditions
    #
    #  @returns         A tuple consisting of the temperatures at the three standard engine stations
    def get_temperatures(self, cea_fostr):
        temperature_results = re.search(r"T, K\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+)", cea_fostr)
        temperature_chamber = float(temperature_results(1))
        temperature_throat  = float(temperature_results(2))
        temperature_exit    = float(temperature_results(3))
        return (temperature_chamber, temperature_throat, temperature_exit)