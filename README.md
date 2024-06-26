# Sankey-Scoping-Review-Application 
## Visualizing Design Choices of Proactive Maintenance Application

This readme file provides an overview of the functionalities and installation possibilities of the provided Sankey app. The program is a Flask-based web application for creating interactive Sankey diagrams. The app allows you to explore and visualize the data flow between different categories or components. The motivation of this application is to facilitate the generation of Sankey diagrams used for scoping and reviewing academic literature.
Once set up, you can:
1. **Interact with the App**
Use the web interface to customize your Sankey diagram. You can select different categories and filters to create the desired visualization.

2. **Generate Sankey Diagram**
After customizing your preferences, click the "Generate Sankey Diagram" button to create and display the Sankey diagram based on your selected criteria.

3. **Explore the Diagram**
You can explore the generated Sankey diagram by interacting with it. Hover over nodes and links to view additional information. You can also save the diagram as an image if needed.

This version of the application is based on the visualization of proactive maintenance design choices. Find one example visualization below.
![newplot (4)](https://github.com/H2020-InnoCyPES-ITN/Sankey-Scoping-Review/assets/101191232/9189a179-c411-4e04-a90c-db44bfec73d8)


# Getting started


### Manual Installation (Windows/Linux/macOS)

1. **Clone the Repository**: Clone this repository to your local machine.
   
   ```python
   git clone https://github.com/your-app-repo.git
   ```
   
2. **Navigate to the Repository**: Change your current directory to the cloned repository.
   ```
   cd sankey-app
   ```

3. **Install Python Packages**: Install the required Python packages using `pip`:
   ```
   pip install -r requirements.txt
   ```
4. **Run the Application**: Start the Sankey App Visualization by running the following command:

- On Windows:

  ```
  python sankey_app.py
  ```

- On Linux/macOS:

  ```
  python3 sankey_app.py
  ```


# Customization
You can customize the Sankey App Visualization by modifying the code to suit your specific data and visualization requirements. The key areas for customization include:

1. **Data Loading:** Modify the data loading section to read data from a different source or format.

2. **Filtering Options:** Adjust the filtering options and criteria to match your dataset.

3. **Color Mapping:** Customize the color mapping to highlight specific nodes or flows.

4. **Node Appearance:** Modify the node appearance settings to change the visual style of the Sankey diagram.

5. **Data Aggregation:** Adjust data aggregation settings to control how flows are combined.

# License
The Sankey App Visualization is provided under an open-source license. You are free to use, modify, and distribute the code as needed, but please review and comply with the specific license terms included in the source code files.

# Acknowledgments
The Sankey App Visualization may include code snippets or libraries from open-source projects. Please acknowledge and respect the licenses and contributions of these projects when using this application.
