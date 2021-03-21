# UCDPA_eoincowhey

# Eoin Cowhey Introductory Certificate in Data Analytics

# Project description: Distribution Transformer Online Monitoring

# Calling external packages, these are pandas an numpy.
import pandas as pd
import numpy as np
# External packages for plot programs are called later.

# Import external .csv Data Files and converting them into DataFrames.
IV_Import = pd.read_csv('CurrentVoltage.csv')
PF_Import = pd.read_csv('PowerFactor.csv')
Temp_Import = pd.read_csv('Temperature.csv')

# Convert Time Format
# The timestamp value is converted from format to an easier format for the user to manipulate later on.
IV_Import['DeviceTimeStamp'] = pd.to_datetime(IV_Import['DeviceTimeStamp'])
PF_Import['DeviceTimeStamp'] = pd.to_datetime(PF_Import['DeviceTimeStamp'])
Temp_Import['DeviceTimeStamp'] = pd.to_datetime(Temp_Import['DeviceTimeStamp'])

# Checking the shape of each data frame.
print(IV_Import.shape)
print(PF_Import.shape)
print(Temp_Import.shape)

# Checking for missing data, missing values for each column on each data set are counted.
missing_val_IV = IV_Import.isnull().sum()
missing_val_PF = PF_Import.isnull().sum()
missing_val_Temp = Temp_Import.isnull().sum()
print(missing_val_IV)
print(missing_val_PF)
print(missing_val_Temp)

# The following code is used to drop duplicate time stamp values.
I_V = IV_Import.drop_duplicates(subset=["DeviceTimeStamp"],).copy()
PF = PF_Import.drop_duplicates(subset=["DeviceTimeStamp"]).copy()
Temp = Temp_Import.drop_duplicates(subset=["DeviceTimeStamp"]).copy()

# The following 3 lines of code are used to remove unnecessary columns in each data set.
I_V = I_V.drop(["VL12","VL23","VL31","INUT"], axis = "columns")
PF = PF.drop(["Avg_PF","Sum_PF","THDVL1","THDVL2","THDVL3","THDIL1","THDIL2","THDIL3","MDIL1","MDIL2","MDIL3"], axis = "columns")
Temp = Temp.drop(["OLI","OTI_A","OTI_T","MOG_A"], axis = "columns")


# Power Calculations

# Merging Current/Voltage Data Frame with Power Factor which is required for Power Calculations
Power_Data_Raw = I_V.merge(PF, on="DeviceTimeStamp", how="left")

# Where time stamps do not line up following left merge, missing Power Factor values are assigned 1 or unity power factor.
Power_Data = Power_Data_Raw.fillna(1)

# To demonstrate the use of functions where the same calculation may be required multiple times.
# Functions are defined for Active and Reactive Power calculations.

# Active Power per phase P = V x I x Cos@
def Watts_Phase(Voltage, Current, PowerFactor):
    return Voltage * Current * PowerFactor

# Reactive Power per phase Q = V x I x sin@
def var_Phase(Voltage, Current, PowerFactor):
    return (Voltage * Current) * np.sin(np.arccos(PowerFactor))

# Active and Reactive Power per phase calculated in Watts and kvar.
Power_Data["WL1"] = Watts_Phase(Power_Data["VL1"],Power_Data["IL1"],Power_Data["PFL1"])
Power_Data["WL2"] = Watts_Phase(Power_Data["VL2"],Power_Data["IL2"],Power_Data["PFL2"])
Power_Data["WL3"] = Watts_Phase(Power_Data["VL3"],Power_Data["IL3"],Power_Data["PFL3"])
Power_Data["varL1"] = var_Phase(Power_Data["VL1"], Power_Data["IL1"], Power_Data["PFL1"])
Power_Data["varL2"] = var_Phase(Power_Data["VL2"], Power_Data["IL2"], Power_Data["PFL2"])
Power_Data["varL3"] = var_Phase(Power_Data["VL3"], Power_Data["IL3"], Power_Data["PFL3"])


# Calculate Total Active Power [kW], Reactive Power [kvar] for each sample using iterrows method.
# This method slows down the program but demonstrates how the itterows function can be used.
kW_total = []
kvar_total = []

for i, row in Power_Data.iterrows():
   kW = (row["WL1"] + row["WL2"] + row["WL3"])/1000
   kvar = (row["varL1"] + row["varL2"] + row["varL3"]) / 1000
   kW_total.append(kW)
   kvar_total.append(kvar)
Power_Data["kW_total"] = kW_total
Power_Data["kvar_total"] = kvar_total


# Calculate Total Apparent Power [kvar] for each sample.
Power_Data["kVA_total"] = (Power_Data["kW_total"]**2 + Power_Data["kvar_total"]**2)**(1/2)


#Subsetting Rows by Date/Time Stamp Range (2019-06-25T13:06 to 2020-04-14T00:30)
Power_Data['Month_Year'] = Power_Data['DeviceTimeStamp'].dt.to_period('M')

# Removing indexes and setting DeviceTimeStamp as the Index.
Power_Data = Power_Data.set_index("DeviceTimeStamp")

print(Power_Data.head())
print(Power_Data.shape)


##### Plotting Charts
#Calling additional packages to be imported for plotting charts.
import seaborn as sns
import matplotlib.pyplot as plt


g = sns.lineplot(x="DeviceTimeStamp", y="kW_total",
                 data=Power_Data,
                 hue="Month_Year")


#Add a title "Average MPG Over Time"
#g.set_title("kW over July 2019")
plt.xticks(rotation=-45)

#g.fig.suptitle("Eoin Cowhey", y=1.02)

g.set(xlabel="Location EC",
      ylabel="% Who Like Techno")


# Show plot
plt.show()



# Code to be deleted
#Power_Data.to_csv("Power_Data.csv")
#July_2019 = Power_Data.loc["2019-09-01T00:00":"2019-09-02T00:00"]
#print(July_2019)