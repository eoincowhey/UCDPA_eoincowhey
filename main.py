# UCDPA_eoincowhey

# Eoin Cowhey Introductory Certificate in Data Analytics

# Project description: Distribution Transformer Online Monitoring

# Import .csv Data Files and converting them into DataFrames
import pandas as pd
import numpy as np

IV_Import = pd.read_csv('CurrentVoltage.csv')
PF_Import = pd.read_csv('PowerFactor.csv')
Temp_Import = pd.read_csv('Temperature.csv')

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

missing_val2 = Power_Data.isnull().sum()
#print(missing_val2)
print(Power_Data.head())
print(Power_Data.dtypes)

#I_V["WL1"] = I_V["VL1"] * I_V["IL1"]
#print(I_V.head())
#I_V["POWL1"] = I_V["VL1"] + I_V["IL1"]
#print(I_V.head())

#Power_Data.to_csv("Power_Data.csv")


#Total Power
Power_Data["WL1"] = Power_Data["VL1"] + Power_Data["IL1"] * Power_Data["PFL1"]
Power_Data["WL2"] = Power_Data["VL2"] + Power_Data["IL2"] * Power_Data["PFL2"]
Power_Data["WL3"] = Power_Data["VL3"] + Power_Data["IL3"] * Power_Data["PFL3"]
Power_Data["kW_total"] = (Power_Data["WL1"] + Power_Data["WL2"] + Power_Data["WL3"])/1000
print(Power_Data.head())



#results_list = []

#for i, row in Power_Data.iterrows():
   #WL1 = row["VL1"] * row["IL1"] #* row["PF"]
   #results_list.append(WL1)

#print(results_list)

#Power_Data["WL1"] = results_list

#print(Power_Data.head())

#def POWER(Voltage, Current, PowerFactor):
    #return Voltage * Current * PowerFactor

#def POWER(Power_Data[])