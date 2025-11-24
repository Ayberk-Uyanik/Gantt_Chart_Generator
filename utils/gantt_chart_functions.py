from datetime import date
import pandas as pd

# Importing Gantt Chart Data #
def get_gantt_chart_data():
    # Gantt Chart Data #
    gantt_chart_data = pd.read_excel(
        "assets/datasets/Timeline.xlsx",
        sheet_name="Timeline_Data"
    )

    return gantt_chart_data

# Colour Assigning #
def assign_conditional_colours(dataframe):
    # Constants #
    condition_list = []
    condition = ""

    # Assigning Conditions #
    for i in range (0, len(dataframe[["Finish_Date"]]), 1):
        if type(dataframe["Notes"][i]) == str:
            if dataframe["Start_Date"][i] > date.today():
                condition = "Planned"
            elif dataframe["Start_Date"][i] <= date.today() and dataframe["Finish_Date"][i] >= date.today():
                condition = "Ongoing"
            elif dataframe["Finish_Date"][i] < date.today():
                condition = "Finished"

        condition_list.append(condition)

    dataframe["Condition"] = condition_list

    # Define color mapping for completed tasks
    #color_mapping = {"Ongoing": "rebeccapurple", "Finished": "gray", "Planned":"darkturquoise", "Delayed":"brown"}
    color_mapping = {"Ongoing": "green", "Finished": "gray", "Planned":"darkturquoise", "Delayed":"brown"}

    # Map the "Condition" column to colors
    dataframe["Colour"] = dataframe["Condition"].map(color_mapping)

    return dataframe

# Remove Nan Values from the Costs Section #
def remove_nan_values(dataframe):
    dataframe = dataframe[["Task", "Colour"]]
    dataframe = dataframe.dropna().reset_index(drop=True)
    
    return dataframe

def display_gantt_chart(dataframe, type):
    # Importing necessary libraries
    import plotly.express as px

    # Figure Constants #
    templates = [
        "plotly", 
        "plotly_white", 
        "plotly_dark", 
        "ggplot2", 
        "seaborn", 
        "simple_white", 
        "none"
    ]

    discrete_map_resource = {
        "Ongoing": "rebeccapurple", 
        "Finished": "gray", 
        "Planned":"darkturquoise", 
        "Delayed":"brown"
    }

    # Dataframe Filtering Based on Type of Work #
    if type == "All":
        dataframe = dataframe
    elif type == "Technical":
        dataframe = dataframe.loc[dataframe["Type"]=="Technical"].reset_index(drop=True)
    elif type == "Commercial":
        dataframe = dataframe.loc[dataframe["Type"]=="Commercial"].reset_index(drop=True)
    
    # Figure Initiation #
    fig = px.timeline(
        dataframe, 
        x_start="Start_Date", 
        x_end="Finish_Date", 
        y="Task", 
        color="Condition", 
        color_discrete_map=discrete_map_resource, 
        template="plotly", 
        text="Notes"
    )
  
    # Add Today's Date #
    fig.add_vline(
        x=date.today(), 
        line_width=3, 
        line_dash="solid", 
        line_color="green"
    )

    # Annotate quarters of the year on top of the figure
    years_names = ["2025", "2026", "2027"]
    years_dates = ["2025-06-30", "2026-06-30", "2027-06-30"]
    quarters_names = ["Q1", "Q2", "Q3", "Q4",
                    "Q1", "Q2", "Q3", "Q4",
                    "Q1", "Q2", "Q3", "Q4",
                    "Q1", "Q2", "Q3", "Q4"]
    quarters_dates = ["2025-02-15", "2025-05-15", "2025-08-15", "2025-11-15",
                    "2026-02-15", "2026-05-15", "2026-08-15", "2026-11-15",
                    "2027-02-15", "2027-05-15", "2027-08-15", "2027-11-15",
                    "2025-02-15", "2025-05-15", "2025-08-15", "2025-11-15"]
    quarter_boundary_dates = ["2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31", 
                            "2026-03-31", "2026-06-30", "2026-09-30", "2026-12-31",
                            "2027-03-31", "2027-06-30", "2027-09-30", "2027-12-31",
                            "2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31"]

    # Add Quarter Names #
    for i in range(0, len(quarters_dates), 1):
        fig.add_annotation(
            text=quarters_names[i],
            x=quarters_dates[i],
            y=-1.5, 
            showarrow=False,
            font=dict(color="black", size=12)
        )

    # Add Years #
    for i in range(0, len(years_dates), 1):
        fig.add_annotation(
            text=years_names[i],
            x=years_dates[i],
            y=-3, 
            showarrow=False,
            font=dict(color="black", size=16)
        )

    # Add Horizontal Lines for Separation of Quarters #
    fig.add_hline(y=-1, line_dash="solid", line_width=0.5)
    fig.add_hline(y=-2, line_dash="solid", line_width=0.5)
    fig.add_hline(y=-4, line_dash="solid", line_width=0.5)

    # Add Vertical Lines for Separation of Quarters #
    for i in range(0, len(quarter_boundary_dates), 1):
        fig.add_shape(
            type="rect",
            x0=quarter_boundary_dates[i], 
            x1=quarter_boundary_dates[i], 
            y0=-1,
            y1=-2,
            line=dict(
                color="black",
                width=0.75,
                )
        )

    # Add Vertical Lines for Separation of Years #
    quarter_boundary_dates_for_years = [
        "2025-12-31", 
        "2026-12-31", 
        "2027-12-31"
    ]

    for i in range(0, len(quarter_boundary_dates_for_years), 1):
        # fig.add_vline(x=i, line_width=0.5, line_dash="solid")
        fig.add_shape(
            type="rect",
            x0=quarter_boundary_dates_for_years[i], 
            x1=quarter_boundary_dates_for_years[i], 
            y0=-2,
            y1=-4,
            line=dict(
                color="black",
                width=0.75,
                )
        )        

    # Customize the layout
    fig.update_layout(
        title=dict(
            text=f"{type} Based Gantt Chart {date.today()}", 
            x=0.5, 
            font=dict(size=20)
        ), 
        width=1500, 
        height=1050, 
        showlegend=True,
        barmode="stack",
        margin_pad=1,
        template="seaborn"
    )

    fig.update_traces(textposition="outside")

    # Y Axis Styles #
    for i in range (0, len(dataframe["Colour"]), 1):
        fig.update_yaxes(
            title=dict(
                text=f"{type} Tasks", 
                font=dict(
                        color="black"
                    )
                ), 
                autorange="reversed", 
                showgrid=True, 
                anchor="free", 
                side="left", 
                spikemode="across", 
                categoryorder="array", 
                categoryarray=dataframe["Task"]
        )

    # X-Axis Styles #
    fig.update_xaxes(
        title=dict(
            text="Dates"
        ), 
        range=["2025-01-01", "2028-01-01"]
    )

    config = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'custom_image',
            'scale':6 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }
    
    fig.show(config=config)