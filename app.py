import plotly.express as px
from shiny import render
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req


ui.page_opts(title="Sarah's Penguin Data", fillable=True)
    
with ui.sidebar(open="open"):  
        ui.h2("Sidebar")
        
        ui.input_selectize(  
        "selectize",  
        "Select an option below:",  
        ["Adelie", "Gentoo", "Chinstrap"],
    )
        ui.input_numeric("plotly_bin_count", "Bin Count", 10, min=1, max=20)
        (ui.input_slider("seaborn_bin_count", "Seaborn Slider", 0, 50, 25),)

        ui.input_checkbox_group(  
        "checkbox_group",  
        "Checkbox group",  
        {  
        "bill_depth_mm":"Bill Depth",  
        "flipper_length_mm": "Flipper Length",  
        "body_mass_g": "Body Mass",  
        },  
    )  

        ui.input_checkbox_group(  
        "selected_species_list",  
        "Select Species",  
        ["Adelie", "Gentoo", "Chinstrap"],
    )  
        ui.hr()
        ui.a(
        "GitHub",
         href="https://github.com/sapapesh/cintel-02-data",
         target="_blank",
         )

with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True):
        "Penguins Table"

    @render.data_frame
    def penguins_datatable():
        return render.DataTable(filtered_data())

with ui.layout_columns(col_widths=(4, 8)):           
    with ui.card(full_screen=True): "Penguins Grid"
    @render.data_frame
    def penguins_data():
        return render.DataGrid(filtered_data(), row_selection_mode="multiple")  

with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True): "Plotly Penguins Histogram"
    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="sex")

with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True): "Seaborn Penguins Histogram"
    @render.plot(alt="Seaborn Histogram", full_page="true")
    def seaborn_histogram():
        histplot = sns.histplot(data=filtered_data(), x="bill_depth_mm", bins=input.seaborn_bin_count())
        histplot.set_title("Palmer Penguins")
        histplot.set_xlabel("Bill Depth")
        histplot.set_ylabel("Count")
        return histplot

with ui.layout_columns(col_widths=(4, 8)):
    with ui.card(full_screen=True): "Plotly Scatterplot"

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(filtered_data(),
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=8, 
        )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]


# Additional Python Notes
# ------------------------

# Capitalization matters in Python. Python is case-sensitive: min and Min are different.
# Spelling matters in Python. You must match the spelling of functions and variables exactly.
# Indentation matters in Python. Indentation is used to define code blocks and must be consistent.

# Functions
# ---------
# Functions are used to group code together and make it more readable and reusable.
# We define custom functions that can be called later in the code.
# Functions are blocks of logic that can take inputs, perform work, and return outputs.

# Defining Functions
# ------------------
# Define a function using the def keyword, followed by the function name, parentheses, and a colon. 
# The function name should describe what the function does.
# In the parentheses, specify the inputs needed as arguments the function takes.

# For example:
#    The function filtered_data() takes no arguments.
#    The function between(min, max) takes two arguments, a minimum and maximum value.
#    Arguments can be positional or keyword arguments, labeled with a parameter name.

# The function body is indented (consistently!) after the colon. 
# Use the return keyword to return a value from a function.

# Calling Functions
# -----------------
# Call a function by using its name followed by parentheses and any required arguments.
    
# Decorators
# ----------
# Use the @ symbol to decorate a function with a decorator.
# Decorators a concise way of calling a function on a function.
# We don't typically write decorators, but we often use them.

