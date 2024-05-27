#%%
"""
Para archivos de Termogravimetria (TG)
Giuliano Basso
https://open.spotify.com/intl-es/track/6710LJA1kZfNM8YM0fQ2gJ?si=d4d1e0ab7ccb4bb6
"""
import os
import numpy as np
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import filedialog
import pandas as pd

#%%
def lector_TG(fpath):
    '''
    Lee archivo txt de la la medida de TG
    Meta: primeras 20 filas
    Data: a partir de fila 22. 
    Time (sec) | Temp (C) | TGA (mg)
    ''' 
    meta = {}
    with open(fpath) as f:
        lines=f.readlines()
        for l in lines:
            if 'Sample Weight' in l: 
                meta['peso_mg']=float(l.split(':')[1].strip('\t[mg]\n'))
            elif 'Sample Name' in l: 
                meta['nombre_de_muestra'] = l.split(':')[1].strip()
            elif 'File Name' in l: 
                meta['nombre_de_archivo'] = l.split(':')[1].strip()
            elif 'Collected Date' in l: 
                meta['fecha'] = l.split(':')[1].strip()
            elif 'Collected Time' in l: 
                meta['tiempo_medida'] = l.split('\t')[-1].strip()
                
    data = pd.read_table(fpath,sep='\t',header=19,
                        names=('time','Temp','TGA'),usecols=(1,2,3),
                        decimal=',',engine='python') 
    data['time'].dropna()
    data['Temp'].dropna()
    data['TGA'].dropna()

    t = pd.Series(data['time']).to_numpy(dtype=float)
    T = pd.Series(data['Temp']).to_numpy(dtype=float)
    TGA = pd.Series(data['TGA']).to_numpy(dtype=float)
    return meta,t,T,TGA
#%% Levanto archivo TG de NPM en acido laurico
meta0,t0,T0,TGA0 = lector_TG(os.path.join(os.getcwd(),'C5140836.TXT'))

meta1,t1,T1,TGA1 = lector_TG(os.path.join(os.getcwd(),'C5231001_Laurico.TXT'))

#busco indices del minimo
indx_min=np.nonzero(TGA0==min(TGA0))
Temp_min=T0[np.nonzero(TGA0==min(TGA0))]
TGA0_min=TGA0[np.nonzero(TGA0==min(TGA0))]
if len(Temp_min)>1 :
    print('Mas de un valor minimo:')
    print(f'T = {Temp_min} °C',f'TG {TGA0_min} mg')
    Temp_min=np.mean(Temp_min)
    TGA0_min=np.mean(TGA0_min)
    print('Se promediarán')


indices_xmin=np.nonzero(T0<=Temp_min-30)[0][-1]
indices_xmax=np.nonzero(T0>=Temp_min+30)[0][0]
TG_porcentual=100*TGA0/meta0['peso_mg']
TG_porcentual_laurico=100*TGA1/meta1['peso_mg']
#%grafico
fig,ax =plt.subplots(constrained_layout=True)
ax.plot(T0,TG_porcentual,'.-',label=meta0['nombre_de_muestra'])
ax.plot(T1,TG_porcentual_laurico,'.-',label=meta1['nombre_de_muestra'])

ax.set_ylabel('Peso (%)')
ax.grid()
ax.set_xlabel('Temperatura (°C)')
ax.legend()


# axins = ax.inset_axes([0.4, 0.4, 0.58, 0.5])
# axins.plot(T0,TG_porcentual,'.-',label=meta0['nombre_de_muestra'])
# # axins.axhline(0,0,1,c='k',lw=0.8)
# # axins.plot(H,m_norm,'.-',label='m norm')
# # axins.plot(H_aux,lineal(H_aux,chi,n),'r-',label=f'$\chi$ = {chi:.3e}\nHc = {H_aux[indx_M]:.3e} A/m')
# # axins.set_xlabel('H (G)')
# axins.grid()
# axins.legend(loc='lower right')
# # axins.legend()
# axins.set_ylim(TG_porcentual[indices_xmin],TG_porcentual[indices_xmax])
# axins.set_xlim(T0[indices_xmin],T0[indices_xmax])
# ax.indicate_inset_zoom(axins, edgecolor="black")
plt.title('TG - Ferrotec en Laurico 80')
#%%
rho=883 #densidad del acido laurico en mg/ml
C0=np.mean(rho*(TGA0[np.nonzero(TGA0==min(TGA0))] - TGA1[np.nonzero(TGA0==min(TGA0))])/TGA0[0])
print(meta0['nombre_de_muestra'],':',f'{C0:.2f}', 'g/L')
#%%

fig,ax =plt.subplots(constrained_layout=True)
ax.plot(T0,TGA0,'.-',label=meta0['nombre_de_muestra'])
ax.plot(T1,TGA1,'.-',label=meta1['nombre_de_muestra'])
ax.axvline(Temp_min,0,1,color='tab:red',label=f'{Temp_min} °C')
#ax.axhline(1.71,0,1,color='k',ls='-.',zorder=-1)
ax.set_ylabel('Peso (%)')
ax.grid()
ax.set_xlabel('Temperatura (°C)')
ax.legend()
plt.title('TGA Ferroresinas')
plt.xlim(Temp_min-30,Temp_min+30)
plt.ylim(0,1.5)
#plt.savefig('TGA_FR.png',dpi=200,facecolor='w')
plt.show()
# %%
