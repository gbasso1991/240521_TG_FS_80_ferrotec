#%%!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Para levantar archivos de TG
@author: giuliano
"""
import os
import numpy as np
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import filedialog
import pandas as pd
#%%

def lector_TA(fpath):
    '''
    Lee archivo txt de la la medida de T
    Data: a partir de fila 16. Time (sec), Temp (C) , TGA (mg)
    ''' 
    data = pd.read_table(fpath,sep='\t',header=16,
                        names=('time','Temp','TA'),usecols=(0,1,2),
                        decimal=',',engine='python') 
    data['time'].dropna()
    data['Temp'].dropna()
    data['TA'].dropna()

    t = pd.Series(data['time']).to_numpy(dtype=float)
    T = pd.Series(data['Temp']).to_numpy(dtype=float)
    TA = pd.Series(data['TA']).to_numpy(dtype=float)
    return t,T,TA

#%% Levanto archivos

directorio= os.getcwd()

fnames=['C6061159.txt','C6120837.txt','C6121153.txt','C6140842.txt']
        
fpath=[fp for fp in [os.path.join(directorio,fn) for fn in fnames]]


#%%

def lector_TG(fpath):
    '''
    Lee archivo txt de la la medida de TG
    Meta: primeras 20 filas
    Data: a partir de fila 22. Time (sec), Temp (C) , TGA (mg)
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

#%%

meta0,t0,T0,TGA0 = lector_TG(fpath[0])
meta1,t1,T1,TGA1 = lector_TG(fpath[1])
meta2,t2,T2,TGA2 = lector_TG(fpath[2])
meta3,t3,T3,TGA3 = lector_TG(fpath[3])

#%% levanto medida de resina sola
fname='C4060956-TA_ResinaSola.txt'

t4,T4,TA4 = lector_TA(os.path.join(directorio,fname))

meta4={'nombre_de_archivo': 'C4060956-TA_ResinaSola.txt',
 'fecha': '12/06/14',
 'tiempo_medida': '08:42:15',
 'nombre_de_muestra': 'Resina s/ NPM',
 'peso_mg': 6.282} 
#%%

TGA0= 100*TGA0/meta0['peso_mg']
TGA1= 100*TGA1/meta1['peso_mg']
TGA2= 100*TGA2/meta2['peso_mg']
TGA3= 100*TGA3/meta3['peso_mg']
TA4= 100*TA4/meta4['peso_mg']
#%%

fig,ax =plt.subplots(constrained_layout=True)
ax.plot(T0,TGA0,'-',label=meta0['nombre_de_muestra'])
ax.plot(T1,TGA1,'-',label=meta1['nombre_de_muestra'])
ax.plot(T2,TGA2,'-',label=meta2['nombre_de_muestra'])
ax.plot(T3,TGA3,'-',label=meta3['nombre_de_muestra'])
ax.plot(T4,TA4,'-',label=meta4['nombre_de_muestra'])

ax.set_ylabel('Peso (%)')
ax.grid()
ax.set_xlabel('Temperatura (°C)')
ax.legend()
plt.title('TGA Ferroresinas')
plt.xlim(20,815)
plt.savefig('TGA_FR.png',dpi=200,facecolor='w')
# plt.show()
# %%
residuo_resina= TA4[-1]

C0= TGA0[-1]-residuo_resina
C1= TGA1[-1]-residuo_resina
C2= TGA2[-1]-residuo_resina
C3= TGA3[-1]-residuo_resina

print(f'{meta0["nombre_de_muestra"]:12s}','%',f'{C0:.3f}')
print(f'{meta1["nombre_de_muestra"]:12s}','%',f'{C1:.3f}')
print(f'{meta2["nombre_de_muestra"]:12s}','%',f'{C2:.3f}')
print(f'{meta3["nombre_de_muestra"]:12s}','%',f'{C3:.3f}')


fig,ax =plt.subplots(constrained_layout=True)
ax.plot(T0,TGA0,'-',label=meta0['nombre_de_muestra'])
ax.plot(T1,TGA1,'-',label=meta1['nombre_de_muestra'])
ax.plot(T2,TGA2,'-',label=meta2['nombre_de_muestra'])
ax.plot(T3,TGA3,'-',label=meta3['nombre_de_muestra'])
ax.plot(T4,TA4,'-',label=meta4['nombre_de_muestra'])
ax.axhline(1.71,0,1,color='k',ls='-.',zorder=-1)
ax.set_ylabel('Peso (%)')
ax.grid()
ax.set_xlabel('Temperatura (°C)')
ax.legend()
plt.title('TGA Ferroresinas')
plt.xlim(790,805)
plt.ylim(0,5)
#plt.savefig('TGA_FR.png',dpi=200,facecolor='w')
plt.show()



# %%
