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
I_V = IV_Import.drop_duplicates(subset=['DeviceTimeStamp'],).copy()
PF = PF_Import.drop_duplicates(subset=['DeviceTimeStamp']).copy()
Temp = Temp_Import.drop_duplicates(subset=['DeviceTimeStamp']).copy()

# The following 3 lines of code are used to remove unnecessary columns in each data set.
I_V = I_V.drop(['VL12','VL23','VL31','INUT'], axis = 'columns')
PF = PF.drop(['Avg_PF','Sum_PF','THDVL1','THDVL2','THDVL3','THDIL1','THDIL2','THDIL3','MDIL1','MDIL2','MDIL3'], axis = 'columns')
Temp = Temp.drop(['OLI','OTI_A','OTI_T','MOG_A'], axis = 'columns')



# Power Calculations

# Merging Current/Voltage Data Frame with Power Factor which is required for Power Calculations.
Power_Data = I_V.merge(PF, on='DeviceTimeStamp', how='left')
# Merging Temperature Data Frame with newly created Power_Data.
Power_Data = Power_Data.merge(Temp, on='DeviceTimeStamp', how='left')

# Where time stamps do not line up following left merge, missing Power Factor values are assigned 1 or unity power factor.
values = {'PFL1': 1, 'PFL2': 1, 'PFL3': 1, 'FRQ': 50}
Power_Data[['PFL1','PFL2','PFL3','FRQ']] = Power_Data[['PFL1','PFL2','PFL3','FRQ']].fillna(value=values)
# For OTI as temperature change is normally slow and predictable, therefore the missing values are forward filled.
Power_Data[['OTI','WTI','ATI']] = Power_Data[['OTI','WTI','ATI']].fillna(method='ffill')

Missing_Power_Data = Power_Data.isnull().sum()
print(Missing_Power_Data)


# To demonstrate the use of functions where the same calculation may be required multiple times.
# Functions are defined for Active and Reactive Power calculations.

# Active Power per phase P = V x I x Cos@
def Watts_Phase(Voltage, Current, PowerFactor):
    return Voltage * Current * PowerFactor

# Reactive Power per phase Q = V x I x sin@
def var_Phase(Voltage, Current, PowerFactor):
    return (Voltage * Current) * np.sin(np.arccos(PowerFactor))

# Active and Reactive Power per phase calculated in Watts and kvar.
Power_Data['WL1'] = Watts_Phase(Power_Data['VL1'],Power_Data['IL1'],Power_Data['PFL1'])
Power_Data['WL2'] = Watts_Phase(Power_Data['VL2'],Power_Data['IL2'],Power_Data['PFL2'])
Power_Data['WL3'] = Watts_Phase(Power_Data['VL3'],Power_Data['IL3'],Power_Data['PFL3'])
Power_Data['varL1'] = var_Phase(Power_Data['VL1'], Power_Data['IL1'], Power_Data['PFL1'])
Power_Data['varL2'] = var_Phase(Power_Data['VL2'], Power_Data['IL2'], Power_Data['PFL2'])
Power_Data['varL3'] = var_Phase(Power_Data['VL3'], Power_Data['IL3'], Power_Data['PFL3'])


# Calculate Total Active Power [kW], Reactive Power [kvar] for each sample using iterrows method.
# This method slows down the program but demonstrates how the itterows function can be used.
kW_total = []
kvar_total = []

for i, row in Power_Data.iterrows():
   kW = (row['WL1'] + row['WL2'] + row['WL3']) / 1000
   kvar = (row['varL1'] + row['varL2'] + row['varL3']) / 1000
   kW_total.append(kW)
   kvar_total.append(kvar)
Power_Data['kW_total'] = kW_total
Power_Data['kvar_total'] = kvar_total


# Calculate Total Apparent Power [kvar] for each sample.
Power_Data['kVA_total'] = (Power_Data['kW_total']**2 + Power_Data['kvar_total']**2)**(1/2)


#Date/Time Stamp Range (2019-06-25T13:06 to 2020-04-14T00:30)
# Creating new column in data frame to assign Month/Year and Month/Year/Day for each sample row.
Power_Data['Month_Year'] = Power_Data['DeviceTimeStamp'].dt.to_period('M')
Power_Data['Month_Year_Day'] = Power_Data['DeviceTimeStamp'].dt.to_period('D')
Power_Data['Time'] = pd.to_datetime(Power_Data['DeviceTimeStamp'])

# Removing indexes and setting DeviceTimeStamp as the Index.
Power_Data = Power_Data.set_index('DeviceTimeStamp')

# Using Numpy to extract summary statistic data from Power Data for each Month
Power_stats = Power_Data.groupby('Month_Year')[['kW_total','kvar_total']].agg([np.min,np.max, np.mean])
print(Power_stats)


# Temperature Calculations
Temperature_stats = Power_Data.groupby('Month_Year')[['OTI','ATI','IL2']].agg([np.min, np.max, np.mean])
print(Temperature_stats)


# Average Ambient Temperature, Oil Temperature and Current (45 minute intervals)
range = pd.date_range('2019-06-25', '2020-04-14', freq='45min')
Temperature_Data = pd.DataFrame(index = range)
Temperature_Data['OTI'] = np.random.randint(low=0, high=51, size=len(Temperature_Data.index))
Temperature_Data['IL2'] = np.random.randint(low=0, high=254, size=len(Temperature_Data.index))
Temperature_Data['ATI'] = np.random.randint(low=0, high=44, size=len(Temperature_Data.index))

print(Temperature_Data.head(100))

def CT_Calc(Current, CT_Primary, CT_Secondary):
    return (Current/CT_Primary)*CT_Secondary

Temperature_Data['I_sec'] =  CT_Calc(Temperature_Data['IL2'],300,1.5)

# To apply temperature rise factors based on current measurement to calculate approximate winding temperature
# with List comprehension.

Temperature_Data['Temp_Comp'] = [0 if i < 0.72 else 10 if i < 0.79 else 12 if i < 0.86 else 14 if i < 0.92
                                else 16 if i < 0.99 else 18 if i < 1.04 else 20 if i < 1.10 else 22
                                if i < 1.15 else 24 if i < 1.21 else 26 if i < 1.26 else 28 if i < 1.31
                                else 30 for i in Temperature_Data['I_sec']]

# Calculate approximate temperature of transformer winding
Temperature_Data['WTI'] = Temperature_Data['OTI'] + Temperature_Data['Temp_Comp']
#Temperature_Data['Month_Year'] = Temperature_Data['DeviceTimeStamp'].dt.to_period('M')
#Temperature_Data.to_csv('Temperature_Data.csv')

# % Loading of the Transformer [Full Load Current IFL = 300 A]
Temperature_Data['%_Loading'] = ((Temperature_Data['IL2'] / 300) * 100).round(decimals=2)



print(Temperature_Data.head())


# Plotting Charts
#Calling additional packages to be imported for plotting charts.

import seaborn as sns
import matplotlib.pyplot as plt


# Graph 1: Average Transformer Active Power Loading
###########################################################################

# Configure graph grid style
sns.set_theme(style='whitegrid')

g = sns.catplot(
    data=Power_Data, kind='bar',
    x='Month_Year', y='kW_total',
    ci=None, palette='dark', alpha=.6, height=6
)

plt.xticks(rotation=-45)
g.despine(left=True)

#Graph Title'
g.fig.suptitle('Average Transformer Active Power Loading', y=0.99)

# Add x-axis and y-axis labels
g.set(xlabel='Year - Month', ylabel='Active Power [kW]')

plt.show()
##########################################################################


# Graph 2: Daily Transformer Reactive Power Loading
###########################################################################
sns.set_theme(style='whitegrid')

g = sns.catplot(
    data=Power_Data, kind='bar',
    x='Month_Year', y='kvar_total',
    ci=None, palette='dark', alpha=.6, height=6
)

plt.xticks(rotation=-45)
g.despine(left=True)

#Graph Title'
g.fig.suptitle('Average Transformer Reactive Power Loading', y=0.99)

# Add x-axis and y-axis labels
g.set(xlabel='Year - Month', ylabel='Reactive Power [kvar]')

plt.show()


###############################################################################

# Graph 3: Daily Transformer Operating Temperature
###############################################################################

# Slicing the day
Date_range = Temperature_Data.loc['2019-09-01 00:00':'2019-09-01 23:59']


fig, ax = plt.subplots()

x = Date_range.index.hour
y1 = Date_range['OTI']
y2 = Date_range['WTI']

ax.plot(x, y1, marker='.', color='r', label='Oil Temperature')
ax.plot(x, y2, marker='.', linestyle=':', color='b', label='Winding Temperature')

plt.xticks(rotation=0)

ax.set_xlabel('Hours')
ax.set_ylabel('Temperature [degC]')

plt.show()

##########################################################################

# Slicing the day


fig, ax = plt.subplots()
ax2 = ax.twinx()

hour = Date_range.index.hour
Oil_Temp = Date_range['OTI']
Wind_Temp = Date_range['WTI']
Loading = Date_range['%_Loading']

ax.plot(hour, Oil_Temp, marker='.', color='r', label='Oil Temperature')
ax2.plot(hour, Loading, color='g', label='% Loading')

#plt.xticks(rotation=-45)

plt.title('Oil Temperature and Loading over 1 Day')

ax.set_xlabel('Hours')
ax.set_ylabel('Temperature [degC]')
ax2.set_ylabel('% of Full Load Current')

print(Date_range)

plt.show()
####################################################################






