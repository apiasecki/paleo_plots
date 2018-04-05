import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pylab import *
from pyteomics import mass # can do cool isotope math stuff, not used here
# plt.style.use('ggplot')
#plt.style.use('presentation')     #have this when i want slides, basically makes it readable from the back row

# import file and make main variables
xls_file = pandas.ExcelFile('data_04_03_18.xlsx')
data  = xls_file.parse('Sheet1')
grims = xls_file.parse('Cgrimsdalei')
prae  = xls_file.parse('Cpraemundulus')
hav   = xls_file.parse('Chavenensis')
mun   = xls_file.parse('Cmundulus')
# labid = xls_file.parse('Sheet2')
vectorz = xls_file.parse('ALLCORES')
# Temperature (using bonifacie)
m = 0.0422
b = 0.2082
data['T'] = ((m*10**6)/(data['D47']-b))**(1/2) - 273.15
T = ((m*10**6)/(data['D47']-b))**(1/2) - 273.15
# Apply ages
age = np.array(vectorz['Age'], dtype=np.float_)
ID = np.array(vectorz['Sample'], dtype=np.float_)
dic = dict(zip(ID, age))

x_all = np.array(data['Sample'], dtype=np.float_)
x_grims = np.array(grims['Sample'], dtype=np.float_)
x_prae = np.array(prae['Sample'], dtype=np.float_)
x_hav = np.array(hav['Sample'], dtype=np.float_)
x_mun = np.array(mun['Sample'], dtype=np.float_)


s = data.shape
data['Age']= 0
for x in range (0, s[0]):
    ID = data.iloc[x,1]
    data.iloc[x,9] = dic[ID]

sg = grims.shape
grims['Age']=0
for x in range (0, sg[0]):
    ID = grims.iloc[x,1]
    grims.iloc[x,8]=dic[ID]

sp = prae.shape
prae['Age']=0
for x in range (0, sp[0]):
    ID = prae.iloc[x,1]
    prae.iloc[x,8]=dic[ID]

sh = hav.shape
hav['Age']=0
for x in range (0, sh[0]):
    ID = hav.iloc[x,1]
    hav.iloc[x,8]=dic[ID]

sm = mun.shape
mun['Age']=0
for x in range (0, sm[0]):
    ID = mun.iloc[x,1]
    mun.iloc[x,8]=dic[ID]

# moving average
avg_num = 20  # needs to be an even number
# moving average for sample oriented stuff
D47_avg = np.convolve(data['D47'], np.ones((avg_num,))/avg_num, mode = 'valid' )
x_int = data['Sample']
l = x_int.shape[0]
MA_X = x_int[(int(avg_num/2)):(l-(int(avg_num/2))+1)]
T_avg = np.convolve(T, np.ones((avg_num,))/avg_num, mode = 'valid' )
# moving average for age oriented stuff
data_A = data.sort_values(['Age'], ascending = True)
D47_avg_A = np.convolve(data_A['D47'], np.ones((avg_num,))/avg_num, mode = 'valid' )
x_int_A = data_A['Age']
l_A = x_int_A.shape[0]
MA_X_A = x_int_A[(int(avg_num/2)):(l_A-(int(avg_num/2))+1)]
T_avg_A = np.convolve(data_A['T'], np.ones((avg_num,))/avg_num, mode = 'valid')
# l_age = x_age.shape[1]
# ma_x_age = x_age[(int(avg_num/2)):(l_age-(int(avg_num/2))+1)]




# data.to_csv('data_out_04_03_18.csv')
# data_A.to_csv('data_A_out_04_03_18.csv')
writer = pandas.ExcelWriter('dataout_040318.xlsx')
data_A.to_excel(writer, sheet_name = 'All')
grims.to_excel(writer, sheet_name = 'grims')
prae.to_excel(writer, sheet_name = 'prae')
hav.to_excel(writer, sheet_name = 'hav')
mun.to_excel(writer, sheet_name = 'mun')

# PLOT TIME
# by age
# d18O plot
plt.figure(figsize = (8,10))
plt.rc('font', family = 'Helvetica')
ax1= plt.subplot2grid((5,3), (0,0), colspan = 3)
ax1.plot(grims['Age'], grims['d18O'], 'bo', label = 'C. grimsdalei')
ax1.plot(prae['Age'], prae['d18O'], 'g^', label = 'C. praemundulus')
ax1.plot(hav['Age'], hav['d18O'], 'rs', label = 'C. havenensis')
ax1.plot(mun['Age'], mun['d18O'], 'kd', label = 'C. mundulus')
ax1.legend(loc = 'best')
ax1.set_ylabel('$\delta^{18}$O (\u2030)')
ax1.invert_yaxis()
# ax1.set_xlim([33.4, 34.6])

# d13C plot
ax2 = plt.subplot2grid((5,3), (1,0), colspan = 3)
ax2.plot(grims['Age'], grims['d13C'], 'bo', label = 'C. grimsdalei')
ax2.plot(prae['Age'], prae['d13C'], 'g^', label = 'C. praemundulus')
ax2.plot(hav['Age'], hav['d13C'], 'rs', label = 'C. havenensis')
ax2.plot(mun['Age'], mun['d13C'], 'kd', label = 'C. mundulus')
ax2.set_ylabel('$\delta^{13}$C (\u2030)')
# ax2.set_xlim([33.4, 34.6])

# ∆47 plot
ax3 = plt.subplot2grid((5,3), (2,0), colspan = 3, rowspan = 2)
ax3.plot(MA_X_A, D47_avg_A, '-', color = 'c', label = 'Moving Average')
ax3.plot(data['Age'], data['D47'], '+', color = '0.75', label = 'Aquisitions', zorder=1)
ax3.set_ylabel('$\Delta_{47}$ (\u2030)')
ax3.legend(loc = 'best')
# ax3.set_xlim([33.4, 34.6])

# T plot
ax4 = plt.subplot2grid((5,3), (4,0), colspan = 3)
# ax4.plot(data_A['Age'], data_A['T'], '-', color = 'm', label = 'Temperature')
ax4.plot(MA_X_A, T_avg_A, '-', color = 'm', label = 'Moving Average')
ax4.set_ylabel('T ($^\circ$C)')
ax4.set_xlabel('Age [Ma]')
ax4.yaxis.set_ticks(np.arange(int(min(T_avg))-1, int(max(T_avg))+1, 2))
# ax4.set_xlim([33.4, 34.6])
plt.grid(True)
plt.savefig('all_04_03_18_time.pdf')


# By Sample ID
# d18O plot
plt.figure(figsize = (8,10))
plt.rc('font', family = 'Helvetica')
ax5= plt.subplot2grid((5,3), (0,0), colspan = 3)
ax5.plot(grims['Sample'], grims['d18O'], 'bo', label = 'C. grimsdalei')
ax5.plot(prae['Sample'], prae['d18O'], 'g^', label = 'C. praemundulus')
ax5.plot(hav['Sample'], hav['d18O'], 'rs', label = 'C. havenensis')
ax5.plot(mun['Sample'], mun['d18O'], 'kd', label = 'C. mundulus')
ax5.legend(loc = 'best')
# ax5.set_xlabel('Sample')
ax5.set_ylabel('$\delta^{18}$O (\u2030)')
ax5.invert_yaxis()
# ax5.set_xlim([6100, 6800])
# ax5.set_ylim([0, 2.5])

# d13C plot
ax6 = plt.subplot2grid((5,3), (1,0), colspan = 3)
ax6.plot(grims['Sample'], grims['d13C'], 'bo', label = 'C. grimsdalei')
ax6.plot(prae['Sample'], prae['d13C'], 'g^', label = 'C. praemundulus')
ax6.plot(hav['Sample'], hav['d13C'], 'rs', label = 'C. havenensis')
ax6.plot(mun['Sample'], mun['d13C'], 'kd', label = 'C. mundulus')
# ax6.legend(loc = 'best')
# ax6.set_xlabel('Sample')
ax6.set_ylabel('$\delta^{13}$C (\u2030)')
# ax6.set_xlim([6100, 6800])
# ax6.set_ylim([0, 2.5])

# ∆47 plot
ax7 = plt.subplot2grid((5,3), (2,0), colspan = 3, rowspan = 2)
ax7.plot(MA_X, D47_avg, '-', color = 'c', label = 'Moving Average')
ax7.plot(data['Sample'], data['D47'], '+', color = '0.75', label = 'Aquisitions', zorder=1)
# ax7.plot(labid['sample'], labid['value'], '.', color = 'k', label = 'Potential Samples')
ax7.set_ylabel('$\Delta_{47}$ (\u2030)')
# ax7.set_xlabel('Sample')
# ax7.set_ylim([0.70, 0.85])
# ax7.set_xlim([6100, 6800])
ax7.legend(loc = 'best')

# T plot
ax8 = plt.subplot2grid((5,3), (4,0), colspan = 3)
ax8.plot(MA_X, T_avg, '-', color = 'm', label = 'Moving Average')
# ax8.set_xlim([6100, 6800])
ax8.set_ylabel('T ($^\circ$C)')
ax8.set_xlabel('Sample')
ax8.yaxis.set_ticks(np.arange(int(min(T_avg))-1, int(max(T_avg))+1, 2))
plt.savefig('all_04_03_18_sample.pdf')

data.to_csv('data_out_04_03_18.csv')
