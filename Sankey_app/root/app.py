
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Assuming we have a pandas DataFrame df
# df = pd.read_csv('your_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from HTML form
        path_elements = request.form.getlist('path_elements')
        color_code = request.form['color_code']
        filters = request.form.getlist('filters')

        # Apply filters and generate sankey data
        # This should be replaced by your own logic
        # For now, we assume sankey_data is generated

        fig = px.sankey(sankey_data,
                        path=path_elements,
                        color_continuous_scale=color_code,
                        title="Sankey Diagram")
        plot_div = fig.to_html(full_html=False)

        return render_template('index.html', plot_div=plot_div)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
