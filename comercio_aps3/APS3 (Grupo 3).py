#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importando as bibliotecas

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# # 2.1 #

# In[2]:


#Importando base itpd
itpd = pd.read_stata(r'C:\Users\david\OneDrive - Insper - Institudo de Ensino e Pesquisa\Insper\6º semestre\Comércio Internacional\APS3\com_int_dados_aps3/itpd.dta')


# In[3]:


#Entendendo a base itpd

itpd.head()


# In[76]:


#Importando base WDICountry

wdi = pd.read_excel(r'C:\Users\david\OneDrive - Insper - Institudo de Ensino e Pesquisa\Insper\6º semestre\Comércio Internacional\APS3\com_int_dados_aps3/WDICountry.xlsx')


# In[77]:


#Entendendo a base wdi

wdi.head()


# ***Item a)***

# In[6]:


#Convertendo para U$bilhões

itpd['trade'] = itpd['trade'] / 10**9


# In[7]:


#Retirando comércio doméstico

itpd = itpd[itpd['exporter_m49'] != itpd['importer_m49']]
itpd.head()


# In[8]:


# Criando Dataframe para exportações
itpd_e = itpd[['exporter_m49','broad_sector','industry_id','year','trade']] #Selecionando variáveis de interesse
itpd_e.rename(columns = {'exporter_m49':'Country','broad_sector':'Industry', 'industry_id': 'Sector','trade':'Export'}, inplace = True) #Renomeando colunas
itpd_e


# In[9]:


# Criando Dataframe para exportações por setor

export_per_sector = itpd_e.groupby(['Country','Industry','Sector','year']).agg(Export=('Export', 'sum'))
export_per_sector.head()


# In[10]:


# Para 2016

exports_i2016 = export_per_sector.xs(2016, level='year')
exports_i2016


# In[11]:


# Analogamente para importações:

itpd_i = itpd[['importer_m49','broad_sector', 'industry_id','year','trade']] #Selecionando variáveis de interesse
itpd_i.rename(columns = {'importer_m49':'Country', 'broad_sector':'Industry', 'industry_id':'Sector','trade':'Import'}, inplace = True) #Renomeando colunas

import_per_sector = itpd_i.groupby(['Country','Industry', 'Sector','year']).agg(Import=('Import', 'sum'))
import_per_sector


# In[12]:


imports_i2016 = import_per_sector.xs(2016, level='year')
imports_i2016


# In[87]:


# Agregando os Dataframes

im_ex2016 = pd.merge(exports_i2016, imports_i2016, left_index=True, right_index=True)

#Resetando o índice
im_ex2016 = im_ex2016.reset_index()
im_ex2016


# ***Item b)***

# In[78]:


# Selecionando as colunas de interesse

wdi = wdi[['Economy','Code','Income group']]

#Retirando as linhas desnecessárias

wdi = wdi.drop(wdi.index[218:])


# In[79]:


wdi


# In[80]:


#Renomeando

wdi.rename(columns = {'Economy':'Country'}, inplace = True)


# In[97]:


im_ex2016m = pd.merge(im_ex2016, wdi, on='Country', how='left')
im_ex2016m


# In[100]:


# Renomeando as colunas
im_ex2016m.rename(columns={'Industry': 'Sector', 'Sector': 'Industry'}, inplace=True)
im_ex2016m


# ***Item c)***

# In[101]:


im_ex2016m['G&L'] = 1 - abs(im_ex2016m['Export'] - im_ex2016m['Import'])/(im_ex2016m['Export'] + im_ex2016m['Import'])
im_ex2016m


# ***Item d)***

# In[20]:


# Categorize as indústrias em dois grandes setores: serviços e não-serviços


# In[102]:


#Separando setores por serviços e não serviços

s_ns = {'Agriculture': 'Não-Serviços', 'Mining & Energy': 'Não-Serviços', 'Manufacturing': 'Não-Serviços', 'Services': 'Serviços'}

im_ex2016m['Type'] = im_ex2016m['Sector'].map(s_ns)
im_ex2016m


# ***Item e)***

# In[103]:


#Vendo categorias de renda

print(im_ex2016m['Income group'].unique())


# In[104]:


# Separando países por renda alta e não alta

r_nr = {'High income': 'Renda alta', 'Low income': 'Renda não-alta', 'Lower middle income': 'Renda não-alta', 'Upper middle income': 'Renda não-alta'}

im_ex2016m['Level'] = im_ex2016m['Income group'].map(r_nr)
im_ex2016m


# ***Item f)***

# In[105]:


# Selecionando as colunas relevantes

hist = im_ex2016m[['G&L', 'Type', 'Level']]
hist


# In[106]:


# Agrupando por setor e nível de renda

hist_grouped = hist.groupby(['Type', 'Level'])
hist_grouped


# In[107]:


#Definindo cores diferentes

colors = ['darkblue', 'darkred', 'darkgreen', 'orange']

# Criando os histogramas

for i, (name, group) in enumerate(hist_grouped):
    sns.histplot(data=group, x='G&L', bins='auto', color=colors[i], kde=True)
    plt.title(f"Histograma do índice de Grubel-Lloyd para {name[0]} e {name[1]}")
    plt.xlabel('Índice de Grubel-Lloyd')
    plt.ylabel('Frequência')
    plt.savefig(f"histograma_{name[0]}_{name[1]}.png")
    plt.show()


# # 2.2 #

# ***Letra a)*** 

# In[108]:


# Lista de países do Mercosul (Venezuela foi suspensa em 2016 e como dados vão até 2016 iremos levá-la em consideração)

merc_coun =['Argentina','Brazil','Paraguay','Uruguay','Venezuela']

export_per_sector = export_per_sector.reset_index()


# In[109]:


# Filtrando dados de exportação para os países do Mercosul

exports_merc = export_per_sector[export_per_sector['Country'].isin(merc_coun)]
exports_merc = exports_merc.reset_index()
exports_merc = exports_merc.drop(columns = 'index')
exports_merc.rename(columns = {'Industry': 'Sector', 'Sector': 'Industry'}, inplace=True)
exports_merc


# In[110]:


# Analogamente para importações:
import_per_sector = import_per_sector.reset_index()
import_per_sector


# In[111]:


# Filtrando dados de exportação para os países do Mercosul

imports_merc = import_per_sector[import_per_sector['Country'].isin(merc_coun)]
imports_merc = imports_merc.reset_index()
imports_merc = imports_merc.drop(columns = 'index')
imports_merc.rename(columns = {'Industry': 'Sector', 'Sector': 'Industry'}, inplace=True)
imports_merc


# In[112]:


# Agregando os Dataframes

im_ex_merc = pd.merge(exports_merc, imports_merc, on = ['Country','Industry','year','Sector'])
im_ex_merc


# ***Item b)***

# In[113]:


#Calculando o índice G&L

im_ex_merc['G&L'] = 1 - abs(im_ex_merc['Export'] - im_ex_merc['Import'])/(im_ex_merc['Export'] + im_ex_merc['Import'])
im_ex_merc


# ***Item c)***

# In[114]:


# Filtrando as indústrias com alto volume de comércio intra-indústria em cada país
gl_mean = im_ex_merc.groupby(['Country', 'Industry'])['G&L'].mean().reset_index()
gl_high = gl_mean[gl_mean['G&L'] > gl_mean.groupby('Country')['G&L'].transform('mean')]

#Indústrias com maior G&L em cada país

gl_pivot = gl_high.pivot_table(index='Country', values='G&L', columns='Industry', aggfunc='max')
print(gl_pivot)


# In[115]:


# Agrupando os dados por país e selecionando a indústria com o maior valor de G&L
gl_max = im_ex_merc.groupby(['Country', 'Industry'])['G&L'].max().reset_index()
idx = gl_max.groupby(['Country'])['G&L'].transform(max) == gl_max['G&L']
gl_max_ind = gl_max[idx]

# Ordenando a tabela por país e valor de G&L
gl_max_ind = gl_max_ind.sort_values(['Country', 'G&L'], ascending=[True, False])

# Exibindo a tabela
print(gl_max_ind)


# In[121]:


im_ex_merc_bloco = im_ex_merc[im_ex_merc['Country'].isin(merc_coun)]
im_ex_merc_bloco_pivot = im_ex_merc_bloco.pivot_table(index='year', columns='Country', values='G&L', aggfunc='mean')
ax = im_ex_merc_bloco_pivot.plot(figsize=(10,6))
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.title('Comércio intra-indústria no Brasil e nos países do Mercosul (média)')
plt.xlabel('Ano')
plt.ylabel('Valor em bilhões de dólares')
plt.savefig('grafico_comercio_intra_industria.png', bbox_inches='tight')
plt.show()

