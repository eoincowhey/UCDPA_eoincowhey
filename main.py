# UCDPA_eoincowhey

# Eoin Cowhey Introductory Certificate in Data Analytics

# Project description: Distribution Transformer Online Monitoring

# Import .csv Data Files and converting them into DataFrames
import pandas as pd
import numpy as np

IV_Import = pd.read_csv('CurrentVoltage.csv')
PF_Import = pd.read_csv('PowerFactor.csv')
Temp_Import = pd.read_csv('Temperature.csv')

#Convert Data and Time Format
IV_Import['DeviceTimeStamp'] = pd.to_datetime(IV_Import['DeviceTimeStamp'])
PF_Import['DeviceTimeStamp'] = pd.to_datetime(PF_Import['DeviceTimeStamp'])
Temp_Import['DeviceTimeStamp'] = pd.to_datetime(Temp_Import['DeviceTimeStamp'])


#print(IV_Import.shape)
#print(PF_Import.shape)
#print(Temp_Import.shape)

# Checking for missing data
missing_val_IV = IV_Import.isnull().sum()
missing_val_PF = PF_Import.isnull().sum()
missing_val_Temp = Temp_Import.isnull().sum()
#print(missing_val_IV)
#print(missing_val_PF)
#print(missing_val_Temp)

I_V = IV_Import.drop_duplicates(subset=["DeviceTimeStamp"],).copy()
PF = PF_Import.drop_duplicates(subset=["DeviceTimeStamp"]).copy()
Temp = Temp_Import.drop_duplicates(subset=["DeviceTimeStamp"])
#I_V.is_copy = False
#print(I_V.shape)
#print(PF.shape)
#print(Temp.shape)

#drop any missing values
#new_data = I_V.dropna()
#new_data = I_V.dropna(subset=["Il1","IL2"]) - drops when only sepecifc colums are null
#new_data = I_V.dropna(axis=1) - drops entire column if a value is missing.
#new_data = I_V.fillna(0) - fills a value with zero if null.
#Cleaned_data = I_V.fillna(method='bfill', axis=0).fillna(0) - fills data with the nest data in the column.

# Subsetting the pertinent columns
#Phase_Voltages = I_V[["DeviceTimeStamp","VL1","VL2","VL1"]]
#Phase_Currents = I_V[["DeviceTimeStamp","IL1","IL2","IL1"]
#Phase_VI = I_V[["DeviceTimeStamp","VL1","VL2","VL1","IL1","IL2","IL3"]]
#PF_phase = PF[["DeviceTimeStamp","PFL1","PFL2","PFL3"]]
#Trafo_Oil_Temp = Temp[["DeviceTimeStamp","OTI"]]
#print(Phase_Voltages.head())
#print(Phase_Currents.head())
#print(PF_phase.head())
#print(Trafo_Oil_Temp.head())

#Phase_VI["WL1"] = Phase_VI["VL1"] + Phase_VI["IL1"] #* Power_Data["PFL1"]
#print(Phase_VI.head())

#Merging Phase_Currents and Trafo_Oil_Temp Together
#Temp_Data = Phase_Currents.merge(Trafo_Oil_Temp, on="DeviceTimeStamp", how="left")
#print(Temp_Data.head())
#print(Temp_Data.shape)
#missing_val = Temp_Data.isnull().sum()
#print(missing_val)

# OTI values not matching time stamps, therefore,
#Cleaned_data = Temp_Data.fillna(method="ffill")
#Cleaned_data_2 = Cleaned_data.isnull().sum()
#print(Cleaned_data_2)
#print(Cleaned_data_2.shape)

#print(Cleaned_data.shape)

#Power Calculations
Power_Data_Raw = I_V.merge(PF, on="DeviceTimeStamp", how="left")
Power_Data = Power_Data_Raw.fillna(1)



#Power_Data.to_csv("Power_Data.csv")

def Watts_Phase(Voltage, Current, PowerFactor):
    return Voltage * Current * PowerFactor

def var_Phase(Voltage, Current, PowerFactor):
    return (Voltage * Current) * np.sin(np.arccos(PowerFactor))

#Total Power
Power_Data["WL1"] = Watts_Phase(Power_Data["VL1"],Power_Data["IL1"],Power_Data["PFL1"])
Power_Data["WL2"] = Watts_Phase(Power_Data["VL2"],Power_Data["IL2"],Power_Data["PFL2"])
Power_Data["WL3"] = Watts_Phase(Power_Data["VL3"],Power_Data["IL3"],Power_Data["PFL3"])
Power_Data["varL1"] = var_Phase(Power_Data["VL1"], Power_Data["IL1"], Power_Data["PFL1"])
Power_Data["varL2"] = var_Phase(Power_Data["VL2"], Power_Data["IL2"], Power_Data["PFL2"])
Power_Data["varL3"] = var_Phase(Power_Data["VL3"], Power_Data["IL3"], Power_Data["PFL3"])


# Calculate Total Active Power [kW], Reactive Power [kvar] for each sample using iterrows method.
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

#Power_Data.to_csv("Power_Data.csv")

#print(Power_Data.head())
#print(Power_Data.shape)

#Subsetting Rows by Date/Time Stamp Range (2019-06-25T13:06 to 2020-04-14T00:30)
Power_Data['Month_Year'] = Power_Data['DeviceTimeStamp'].dt.to_period('M')
Power_Data = Power_Data.set_index("DeviceTimeStamp")

print(Power_Data.head())

# Subsetting and removing indexes
#July_2019 = Power_Data.loc["2019-09-01T00:00":"2019-09-02T00:00"]
#print(July_2019)

#Plotting Charts
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


