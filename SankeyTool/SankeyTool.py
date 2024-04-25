#%%   
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from itertools import product
from functools import reduce
import random
import copy
import os

#%%
def sample_hex(a):
    return "#%06x" % random.randint(0, 0xFFFFFF)

sample_hexes = np.vectorize(sample_hex)
color_link = sample_hexes(np.empty(10000))

def create_sankey_input_dict(df,path):
    
    path_elements = [df[col].drop_duplicates().to_list() for col in path]
    path_elements_combinations = list(product(*path_elements))
    path_elements_idx_dict = dict(zip(np.concatenate(path_elements),list(range(np.concatenate(path_elements).shape[0]))))
    
    
    links = {'source':[],'target':[],'value':[],'color':[],'flow_str':[]}

    for j,combi in enumerate(path_elements_combinations):
        
        # equal
        Ss = [data[path[i]]==combi[i] for i in range(len(combi))]
        
        # str contains (to be used for data and component columns only)
        
        val = df[reduce(lambda x, y: x.multiply(y, fill_value=0), Ss)].shape[0]
        

        if val!=0:
            source_col = 0
            while source_col<len(combi)-1:
                links['source'].append(path_elements_idx_dict[combi[source_col]])
                links['target'].append(path_elements_idx_dict[combi[source_col+1]])
                links['value'].append(val)
                links['flow_str'].append(list(combi))
                links['color'].append(color_link[j])
                source_col +=1
                
    labels = list(path_elements_idx_dict.keys())
    
    return links,labels

def recolor(df,path,links,color_setter_idx,colors=None):
    keys = df[path[color_setter_idx]].drop_duplicates().to_list()
    keys_set = set(keys)
    if colors == None:
        color_dict = dict(zip(keys,color_link[list(range(len(keys)))]))
    else:
        color_dict = dict(zip(keys,colors[list(range(len(keys)))]))
                      
    for i in range(len(links['source'])):
        k = keys_set.intersection(links['flow_str'][i])
        links['color'][i] = color_dict[list(k)[0]]
    return links
#%% Get data



data_org = pd.read_excel(os.path.join(os.path.dirname(__file__),'Result tables.xlsx'),
              sheet_name='Sankey2',header=0) # Requires an excel engine. I use openpyxl


#%%

# Make copy of data such that it can be manipulate over an over, without needing to reload it from the excel. The excel sheet can the remain open after the first read.
data = copy.deepcopy(data_org)

# Fault detection is a subset of condition monitoring
# data.loc[data[data['Function'] == 'Early fault detection'].index,'Function'] = 'Condition monitoring'
# # RUL prediction is a subset of prognosis
# data.loc[data[data['Function'] == 'Remaining useful life prediction'].index,'Function'] = 'Prognosis'

# Formatting Cite key column's cells
for i,row in data.iterrows():
    data.loc[i,'Cite_key'] = '\cite{'+row['Cite_key']+'}'
    
"""Path and color_setter are the two principal hyperparameters that can be change to create different sankey diagrams.
The path defines the sequence of node elements to be included in the sankey. The color_setter defines which of the nodes should be the reference
for coloring the links (flows between nodes)"""

# path = ['Method_category','Method_class','Function','Data']
path = ['Granularity','Component_clean','Function']
# data = data[data.Component_clean=='Transformer']
color_setter = 0

force_data_explosion = True
force_component_explosion = True

if ('Data' in path) | force_data_explosion:
    data = data.assign(Data=data['Data'].str.split(',')).explode('Data')
if 'Component_original' in path:
    data = data.assign(Component_original=data['Component_original'].str.split(',')).explode('Component_original')
if ('Component_clean' in path) | force_component_explosion:
    data = data.assign(Component_clean=data['Component_clean'].str.split(',')).explode('Component_clean')
if 'Granularity' in path:
    data = data.assign(Granularity=data['Granularity'].str.split(',')).explode('Granularity')
if 'Output' in path:
    data = data[~data.Output.isnull()]

# Expressions like this can be used to subset some of the data
data = data[data.Function.isin(['Condition monitoring','Prognosis','Remaining useful life prediction','Early fault detection','Ranking'])]
# If e.g. you were not interested in the 'other' data category, it can be filtered out using:
data = data[~data.Data.isin(['Other'])]


# find links and nodes
links,labels = create_sankey_input_dict(data,path)
# recolor (optional but recommended)
links = recolor(data,path,copy.deepcopy(links),color_setter,None)

# define node dict
node = dict(
  pad = 15,
  thickness = 20,
  line = dict(color = "black", width = 0.5),
  label = labels,
  color = "blue"
)

# Aggregate twin flows
temp = pd.DataFrame({'source':links['source'],
              'target':links['target'],
              'value':links['value'],
              'color':links['color']})
temp = temp.groupby(['source','target','color']).sum().reset_index()
new_links = dict(source=temp['source'],target=temp['target'],value=temp['value'],color=temp['color'])

# Create sankey data object
sankey_data = go.Sankey(node = node, link = new_links)

# plot
fig = go.Figure(sankey_data)
fig.update_layout(
    # hovermode='x',
    # title='Papers on transformers only',
    font=dict(size=12, color='black'),
    
    # Set diagrams background colour to almost black
    # paper_bgcolor='#51504f'
)
fig.show()