#-*- encoding: utf-8 -*-

import pandas as pd
import numpy as np
import os

PROPORTION = 0.05
RANDOM_SEED = 1
# PATH = '../data/sample/population_sample.csv'
PATH = '../data/pop_sample_2.csv'
df = pd.read_csv(PATH, index_col=0)
idx = np.random.choice(df.index.unique(), int(PROPORTION*len(df)), \
						replace=False)
df_sample = df.loc[idx,:]
print(len(df))
print(len(df_sample))
columns = df.columns

df_hometype = df.index.value_counts()
# df_hometype[df_hometype>20] = '21 or above'
df_hometype[df_hometype>7] = '8 or above'
list_hometypes = df_hometype.unique()

tmp_df = pd.DataFrame(df_hometype.value_counts().values,columns=['population'],\
					index=df_hometype.value_counts().index.tolist())
tmp_df['sample'] = 0
tmp = df_sample.index.value_counts()
# tmp[tmp>20] = '21 or above'
tmp[tmp>7] = '8 or above'
df_hometype_sample = tmp.value_counts()
print(df_hometype_sample)
for i in df_hometype_sample.index:
	tmp_df.loc[i, 'sample'] = df_hometype_sample[i]
	tmp_df = tmp_df.loc[list_hometypes,:]
# tmp_df.to_csv('../data/sample/population_sample_hometype.csv')
tmp_df.to_csv('../data/population_sample_2_hometype.csv')
print(tmp_df)
print(list_hometypes)

def get_statistic(df, df_sample, columns):
	
	for col in columns:
		tmp = df[col].value_counts()
		tmp_sample = df_sample[col].value_counts()
		tmp_df = pd.DataFrame(tmp.values,columns=['population'],\
							index=tmp.index.tolist())
		tmp_df['sample'] = 0.0

		for i in tmp_sample.index:
			tmp_df.loc[i, 'sample'] = tmp_sample[i]

		for hometype in list_hometypes:

			tmp_df['population_{}'.format(hometype)] = 0.0
			tmp_df['sample_{}'.format(hometype)] = 0.0
			df_home, df_home_sample = get_df_by_home(df, df_sample,\
								col, hometype)

			for i in df_home.index:
				tmp_df.loc[i,'population_{}'.format(hometype)] = df_home[i]
				if i in df_home_sample.index:
					tmp_df.loc[i,'sample_{}'.format(hometype)] = df_home_sample[i]

		# tmp_df.to_csv('../data/sample/population_sample_{}.csv'.format(col))
		tmp_df.to_csv('../data/population_sample_{}.csv'.format(col))

def get_df_by_home(df, df_sample, col, hometype):

	idx = df_hometype[df_hometype==hometype].index.tolist()
	df_home = df.loc[idx,col]
	idx = set(idx) & set(df_sample.index) 
	df_home_sample = df_sample.loc[list(idx),col]

	return df_home.value_counts(), df_home_sample.value_counts()

if __name__ == '__main__':
	get_statistic(df, df_sample, columns)


	
