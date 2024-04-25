# Import the requiered modules
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from itertools import product
from functools import reduce
import random
import copy
import os
import webview
import logging
import random
logging.basicConfig(filename='app.log', level=logging.DEBUG)


def launch_flask_app():
    # Create a Flask app instance
    app_instance = app

    # Start the webview window
    webview.create_window("My Flask App", app_instance, width=1600, height=1000)
    webview.start()


app = Flask(__name__)

def sample_hex(a):
    """
    Returns a random hexadecimal color code.

    Args:
    a (int): An integer value.

    Returns:
    str: A string representing a hexadecimal color code.

    Example:
    >>> sample_hex(1)
    '#f6d2a3'
    """
    # Generate a random integer between 0 and 0xFFFFFF (16777215 in decimal)
    # and format it as a hexadecimal string with 6 digits (including leading zeros)
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
        Ss = [df[path[i]]==combi[i] for i in range(len(combi))]
        
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

# Assuming we have a pandas DataFrame df
data_org = pd.read_excel('data/Result tables.xlsx',
              sheet_name='Input Data',header=0) # Requires an excel engine. I use openpyxl

filters = {col: data_org[col].unique().tolist() for col in data_org[["Method_class", "Component_category", "Function"]].columns} 

@app.route('/', methods=['GET', 'POST'])
def index():

    
    selected_values = {
            'dropdown1': "Granularity",
            'dropdown2': "Component_category",
            'dropdown3': "Function",
            'dropdown4': "",
            'dropdown5': ""
        }

    selected_filters = {
            'dropdown1': "",
            'dropdown2': "",
            'dropdown3': "",
            'dropdown4': "",
            'dropdown5': ""
        }

    color_setter = 0 

    if request.method == 'POST':

        selected_values = {
            'dropdown1': request.form.get('dropdown1'),
            'dropdown2': request.form.get('dropdown2'),
            'dropdown3': request.form.get('dropdown3'),
            'dropdown4': request.form.get('dropdown4'),
            'dropdown5': request.form.get('dropdown5')
        }


        selected_filters = {category: request.form.get(category) for category, options in filters.items()}

        """Path and color_setter are the two principal hyperparameters that can be change to create different sankey diagrams.
        The path defines the sequence of node elements to be included in the sankey. The color_setter defines which of the nodes should be the reference
        for coloring the links (flows between nodes)"""

        path = [value for value in selected_values.values() if value != '']

        color_setter = int(request.form.get('color_selector'))

        data = copy.deepcopy(data_org)



        force_data_explosion = True
        force_component_explosion = True

        if ('Data' in path) | force_data_explosion:
            data = data.assign(Data=data['Data'].str.split(',')).explode('Data')
        if 'Component_original' in path:
            data = data.assign(Component_original=data['Component_original'].str.split(',')).explode('Component_original')
        if ('Component_category' in path) | force_component_explosion:
            data = data.assign(Component_category=data['Component_category'].str.split(',')).explode('Component_category')
        if 'Granularity' in path:
            data = data.assign(Granularity=data['Granularity'].str.split(',')).explode('Granularity')
        if 'Output' in path:
            data = data[~data.Output.isnull()]

        #Expressions like this can be used to subset some of the data
        #data = data[data.Function.isin(['Condition monitoring','Prognosis','Remaining useful life prediction','Early fault detection','Ranking'])]

        for category, filter_value in selected_filters.items():
            if filter_value:  # Check if filter_value is not None or empty
                data = data[data[category] == filter_value]
        
        #If e.g. you were not interested in the 'other' data category, it can be filtered out using:
        data = data[~data.Data.isin(['Other'])]


        # find links and nodes
        links,labels = create_sankey_input_dict(data,path)
        # recolor (optional but recommended)
        links = recolor(data,path,copy.deepcopy(links),color_setter,None)

        # define node dict
        node = dict(
        pad = 15,
        thickness = 30,
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
            title=' Sankey Diagramm: ' + str(path) + "Filter" + str(selected_filters),
            font=dict(size=18, color='black'),
            titlefont=dict(size=15, color='black'),
        )

        

        plot_div = fig.to_html(full_html=False)

        return render_template('index.html', plot_div=plot_div, columns=data_org.columns.tolist(), path = path, selected_values=selected_values, color_setter= color_setter, filters = filters, selected_filters=selected_filters, table_div = data[["Reference Number", "Reference Title"]].drop_duplicates().to_html(index=False))

    return render_template('index.html', columns=data_org.columns.tolist(), selected_values=selected_values, filters = filters, selected_filters=selected_filters)



if __name__ == "__main__":
    #app.run(debug= False, host="localhost", port=5000)
    launch_flask_app()