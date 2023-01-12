import numpy               as np
import pandas              as pd
import time
from   CeaDatasetGenerator import CeaDatasetGenerator

fuels = ["CH4", "RP-1", "MeOH", "EtOH", "LH2", "N2H4", "MMH", "UDMH", "Aerozine-50"]
oxids = ["LOX", "N2O4", "HNO3", "RFNA", "H2O2"]

# Cards to add to CeaDatasetGenerator:
#   - fuels: MeOH, EtOH, Aerozine-50
#   - oxids: RFNA (83.5% HNO3, 14% NTO, 2.5% H2O)

for fuel in fuels:
    for oxidizer in oxids:
        dataset_gen = CeaDatasetGenerator(fuel, oxidizer, n=100_000)


        output_filename = f"RawData/{fuel}_{oxidizer}.csv"