# Imported from shared Colab Notebook. Contributors: Andy Hoang, Henry Tam, Son Dang, Nikita Yadav

import plotly.graph_objects as go

fig = go.Figure(go.Sankey(
    arrangement="snap",
    node={
        'pad': 15,
        'thickness': 20,
        'line': dict(color="white", width=0),
        'label': ["Seattle", "Bainbridge Island (2018)", "Bainbridge Island (2019)", "Bainbridge Island (2020)", "Bainbridge Island (2021)", "Bainbridge Island (2022)"],
        'x': [0.0001,0.9999,0.9999,0.9999, 0.9999, 0.9999],
        'y': [0.0001,0.0001, 1/6, 2/6, 3/6],
        'color': ["#003060","green", "#92b4e3", "red", "#628dd6", "#4c74c9"]
    },
    link={
        'source': [0, 0, 0, 0, 0],
        'target': [1, 2, 3, 4, 5],
        'color': ["#abbcea", "#92b4e3", "#7ba4dd", "#628dd6", "#4c74c9",],
        'value': [6355278, 6212828, 2579032, 3717188, 4435933]
    }))

legend_colors = ["green", "red"]

legend_years = ["Highest Total Riders", "Lowest Total Riders"]

for x in range(len(legend_colors)):
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=12, color=legend_colors[x]),
        name=legend_years[x],
        legendgroup="group",
    ))


caption_text = 'The ferries are in trouble! As of January 17th of this year,<br>' \
               'Washington State Ferries needs more boats and more staff.<br>' \
               'Ferry ridership has not caught up to pre-pandemic levels,<br>' \
               'yet the vessel and staff shortages are still causing trouble<br>' \
               'for WSF.'

caption_annotation = dict(
    x=1,
    y=-0.19,
    xref='paper',
    yref='paper',
    text=caption_text,
    showarrow=False,
    font=dict(size=12, color='black'))

data_source = '<i>Data Source: Washington State Department of Transportation(WSDOT)<i>'
data_access = '<i>Date Accessed: January 16, 2024<i>'
copyright = '<i>Copyright WSDOT © Washington Technology Solutions<i>'

fig.update_layout(title_text="<b>Total Amount of Ferry Riders taken from Seattle to Bainbridge Island Per Year (2018-2022)<b>",
                  font_size = 15,
                  annotations=[caption_annotation,
                               dict(x=-0.09, y=-0.166, xref='paper', yref='paper', text=copyright, showarrow=False, font=dict(size=8.5, color='black')),
                               dict(x=-0.09, y=-0.19, xref='paper', yref='paper', text=data_source, showarrow=False, font=dict(size=8.5, color='black')),
                               dict(x=-0.09, y=-0.14, xref='paper', yref='paper', text=data_access, showarrow=False, font=dict(size=8.5, color='black'))],
                  showlegend=True,
                  height=600,
                  width=1200,
                  legend=dict(x=1, y=0.43)
                  )

fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)

fig.show()
