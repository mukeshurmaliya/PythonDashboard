import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DASHBBGCOL = "#20283E"
CHARTCOLOR = "lightblue"
CHARTXTCOL = "purple"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the Dashboard
app.layout =  html.Div(
    style={
        "height": "100vh",  # Full viewport height
        "width": "100vw",   # Full viewport width
        "margin": "0",      # Remove default margin
        "padding": "0",     # Remove default padding
        "display": "flex",  # Flexbox for alignment
        "justifyContent": "center",  # Center horizontally
        "alignItems": "center",  # Center vertically
        "backgroundColor": DASHBBGCOL,  # Light gray background
        "color": "white"
    },
    children=[
    dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(style={"width": "125px","height": "100px", "backgroundColor": "#20283E","border": "2px solid black", "borderRadius": "5px", "display": "flex","alignItems": "center","justifyContent": "center","color": "white", "fontSize": "23px" },children="Customer Experience Dashboard")
        ], width=1),
        dbc.Col([
            dcc.Graph(id='TOTDDATA_fig')
        ], width=10),
        dbc.Col([
            html.H1("MVP", style={'textAlign': 'center','fontFamily': 'arial','fontSize': 23,'fontWeight': 'bold','color': 'yellow'})
            #html.Div(style={"width": "200px","height": "100px", "backgroundColor": "#20283E","border": "2px solid black", "borderRadius": "0px", "display": "flex","alignItems": "center","justifyContent": "center","color": "white", "fontSize": "25px" },children="")
        ], width=1)                
    ], style={"height": "100px", "background-color": DASHBBGCOL}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='MAINKQIS_fig'),
        ], width=1),
        dbc.Col([
            dcc.Graph(id='DTSR_fig'),
        ], width=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='DTADUCT_fig'),
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='DTADRCT_fig'),
                ], width=6)
            ]),
            dbc.Row([
            dcc.Graph(id='ROAMWMAP_fig'),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='TOPDVBR_fig'),
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='TOPOTCON_fig'),
                ], width=6)

            ], style={"background-color": DASHBBGCOL}),  
       ], width=8)
    ], style={"background-color": "488A99"}),

    # Define Auto-refresh Interval for every 10 seconds
    dcc.Interval(
        id='interval-component',
        interval=10000,  # 10000 ms = 10 seconds
        n_intervals=0
    )
 ]
, fluid=True
)
])

# Callback to update all charts
@app.callback(
    Output('TOTDDATA_fig', 'figure'),
    Output('MAINKQIS_fig', 'figure'),
    Output('DTSR_fig', 'figure'),
    Output('DTADUCT_fig', 'figure'),
    Output('DTADRCT_fig', 'figure'),
    Output('TOPDVBR_fig', 'figure'),
    Output('TOPOTCON_fig', 'figure'),
    Output('ROAMWMAP_fig', 'figure'),        
    Input('interval-component', 'n_intervals')
)

def update_charts(n):
    # Load data from CSV Files for different KQIs and Metrics
    countrycodes = pd.read_csv("RKTISOcodes.csv")
    mainkpis = pd.read_csv("RKTMainKPIs.csv")
    DDASR = mainkpis.iloc[-1]['DDASR']
    DVCSR = mainkpis.iloc[-1]['DVCSR']
    DWRSR = mainkpis.iloc[-1]['DWRSR']
    DVCST = mainkpis.iloc[-1]['DVCST']
    DVQMOS = mainkpis.iloc[-1]['DVQMOS']
    DSSR = mainkpis.iloc[-1]['DSSR']
    devtypes = pd.read_csv("RKTDeviceTypes.csv")
    topbrnds = pd.read_csv("RKTTopBrands.csv")
    topoapps = pd.read_csv("RKTTopOTT.csv")
    topcntrs = pd.read_csv("RKTTopCountries.csv")
    roagmaps = pd.read_csv("RKTRoamingMap.csv")
    rdtotdat = pd.read_csv("RKTDailyTotalData.csv") 
    DTAUMIL = rdtotdat.iloc[0]['DTAUMIL']
    DTDTB = rdtotdat.iloc[0]['DTDTB']     
    DTVCMIL = rdtotdat.iloc[0]['DTVCMIL']  
    DTAIUMIL = rdtotdat.iloc[0]['DTIAUMIL']
    DTIDTB = rdtotdat.iloc[0]['DTIDTB']     
    DTIVCMIL = rdtotdat.iloc[0]['DTIVCMIL']   
    devtypes = devtypes.sort_values(by="Share", ascending=False)
    topbrnds = topbrnds.sort_values(by="Share", ascending=False)
    topoapps = topoapps.sort_values(by="Share", ascending=True).head(6)
    topcntrs = topcntrs.sort_values(by="Share", ascending=True).head(6)

    ##################################################### Status Color DDASR ###########################################
    if DDASR >= 99:
        DDASRCLR = "darkgreen"
    elif DDASR >= 95:
        DDASRCLR = "yellow"
    elif DDASRCLR >= 90:
        DDASRCLR = "darkorange"
    else:
        DDASRCLR = "red"

    def getStatusClr(curvalue,warnlevel,critlevel):
        if curvalue >= int(critlevel):
            return "lightgreen"
        elif curvalue >= int(warnlevel):
            return "darkorange"
        else:
            return "red"

    ##################################################### Gauge Meter  ##################################################
    ## Gauge Meter to present Total Daily Data in a Sub Plot
    ##################################################### Gauge Meter ##################################################
    TOTDDATA_fig = make_subplots(rows=1, cols=6, specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]])
    ##TOTDDATA_fig.add_trace(go.Indicator(title={"text": "👥 Daily Active Users (Mil)", "font": {"size": 14, "color": "white"}},mode="gauge+number",value=DTAUMIL, gauge={"axis": {"range": [0, 100], "tickcolor": "white"},  "bar": {"color": "cyan"}, "bgcolor": "#333333"}), row=1, col=1)
    TOTDDATA_fig.add_trace(go.Indicator(title={"text": "👥 Active Users (Mil)", "font": {"size": 18, "color":"white"}},mode="number",value=DTAUMIL), row=1, col=1)
    TOTDDATA_fig.add_trace(go.Indicator(title={"text": "💾 Daily Total Data (TB)", "font": {"size": 18, "color":"white"}},mode="number",value=DTDTB), row=1, col=2)
    TOTDDATA_fig.add_trace(go.Indicator(title={"text": "📞 Daily Calls (Mil)", "font": {"size": 18, "color":"white"}},mode="number",value=DTVCMIL), row=1, col=3)
    TOTDDATA_fig.add_trace(go.Indicator(title={"text": "👥 IR Active Users (Mil)", "font": {"size": 18, "color":"white"}},mode="number",value=DTAIUMIL), row=1, col=4)
    TOTDDATA_fig.add_trace(go.Indicator(title={"text": "💾 IR Total Data (TB)", "font": {"size": 18, "color":"white"}},mode="number",value=DTIDTB), row=1, col=5)
    TOTDDATA_fig.add_trace(go.Indicator(title={"text": "📞 IR Calls (Mil)", "font": {"size": 18, "color":"white"}},mode="number",value=DTIVCMIL), row=1, col=6)
    TOTDDATA_fig.update_layout(height=100, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=40, b=10),
                                   shapes=[
        # Background for row 1
        dict(type="rect", x0=0, x1=0.15, y0=0, y1=1, xref="paper", yref="paper",
             fillcolor=getStatusClr(DTAUMIL,4,5), layer="below", line_width=0),
        # Background for row 2
        dict(type="rect", x0=0.16, x1=0.33, y0=0, y1=1, xref="paper", yref="paper",
             fillcolor=getStatusClr(DTDTB,1000,1200), layer="below", line_width=0),
        # Background for column 1
        dict(type="rect", x0=0.34, x1=0.50, y0=0, y1=1, xref="paper", yref="paper",
             fillcolor=getStatusClr(DTVCMIL,15,20), layer="below", line_width=0),
        # Background for row 1
        dict(type="rect", x0=0.51, x1=0.67, y0=0, y1=1, xref="paper", yref="paper",
             fillcolor=getStatusClr(DTAIUMIL,4,5), layer="below", line_width=0),
        # Background for row 2
        dict(type="rect", x0=0.68, x1=0.84, y0=0, y1=1, xref="paper", yref="paper",
             fillcolor=getStatusClr(DTIDTB,1000,1200), layer="below", line_width=0),
        # Background for column 1
        dict(type="rect", x0=0.85, x1=1, y0=0, y1=1, xref="paper", yref="paper",
             fillcolor=getStatusClr(DTIVCMIL,1,2), layer="below", line_width=0)
    ],
                               )
    ##################################################### Gauge Meter  ##################################################

    ##################################################### Gauge Meter  ##################################################
    ## Gauge Meter to present Keey KPIs
    ##################################################### Gauge Meter ##################################################
    MAINKQIS_fig = make_subplots(rows=6, cols=1, specs=[[{"type": "indicator"}], [{"type": "indicator"}], [{"type": "indicator"}], [{"type": "indicator"}], [{"type": "indicator"}], [{"type": "indicator"}]])
    MAINKQIS_fig.add_trace(go.Indicator(title={"text": "Accessibility SR", "font": {"size": 12, "color":"black"}},mode="number",value=DDASR,number={"font": {"size": 40}}), row=1, col=1)
    MAINKQIS_fig.add_trace(go.Indicator(title={"text": "Call Setup SR", "font": {"size": 12, "color":"black"}},mode="number",value=DVCSR,number={"font": {"size": 40}}), row=2, col=1)
    MAINKQIS_fig.add_trace(go.Indicator(title={"text": "Web Response SR", "font": {"size": 12, "color":"black"}},mode="number",value=DWRSR,number={"font": {"size": 40}}), row=3, col=1)
    MAINKQIS_fig.add_trace(go.Indicator(title={"text": "Voice Call Setup", "font": {"size": 12, "color":"black"}},mode="number",value=DVCST,number={"font": {"size": 40}}), row=4, col=1)
    MAINKQIS_fig.add_trace(go.Indicator(title={"text": "Video Quality", "font": {"size": 12, "color":"black"}},mode="number",value=DVQMOS,number={"font": {"size": 40}}), row=5, col=1)
    MAINKQIS_fig.add_trace(go.Indicator(title={"text": "SMS Success Rate", "font": {"size": 12, "color":"black"}},mode="number",value=DSSR,number={"font": {"size": 40}}), row=6, col=1)
    MAINKQIS_fig.update_layout(height=1000, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=40, b=10),
                                   shapes=[
        # Background for row 1
        dict(type="rect", x0=0, x1=1, y0=0.02, y1=0.14, xref="paper", yref="paper",
             fillcolor=getStatusClr(DSSR,95,98), layer="below", line_width=0),
        # Background for row 2
        dict(type="rect", x0=0, x1=1, y0=0.19, y1=0.31, xref="paper", yref="paper",
             fillcolor=getStatusClr(DVQMOS,4,5), layer="below", line_width=0),
        # Background for column 1
        dict(type="rect", x0=0, x1=1, y0=0.36, y1=0.48, xref="paper", yref="paper",
             fillcolor=getStatusClr(DVCST,1.5,1.8), layer="below", line_width=0),
        # Background for row 1
        dict(type="rect", x0=0, x1=1, y0=0.53, y1=0.65, xref="paper", yref="paper",
             fillcolor=getStatusClr(DWRSR,95,98), layer="below", line_width=0),
        # Background for row 2
        dict(type="rect", x0=0, x1=1, y0=0.70, y1=0.82, xref="paper", yref="paper",
             fillcolor=getStatusClr(DVCSR,95,98), layer="below", line_width=0),
        # Background for column 1
        dict(type="rect", x0=0, x1=1, y0=0.87, y1=0.99, xref="paper", yref="paper",
             fillcolor=getStatusClr(DDASR,95,98), layer="below", line_width=0)
    ],
                               )
    ##################################################### Gauge Meter  ##################################################

    ##################################################### Scatter Chart ##################################################
    ## Top 6 Main KQIs in a Sub Plot
    ##################################################### Scatter Chart ##################################################
    DTSR_fig = make_subplots(rows=6, cols=1, specs=[[{"type": "scatter"}], [{"type": "scatter"}], [{"type": "scatter"}], [{"type": "scatter"}], [{"type": "scatter"}], [{"type": "scatter"}]],subplot_titles=("Accesiility SR Trend", "Call Setup SR Trend", "Web Response SR Trend", "Voice Call Setup Trend", "Video Quality Trend", "SMS Succeess Rate Trend"))
    DTSR_fig.add_trace(go.Scatter(x=mainkpis["Date"], y=mainkpis["DDASR"], mode="markers+lines", marker=dict(color=CHARTCOLOR),line=dict(shape='spline', smoothing=1.3)), row=1, col=1)
    DTSR_fig.add_trace(go.Scatter(x=mainkpis["Date"], y=mainkpis["DVCSR"], mode="markers+lines", marker=dict(color=CHARTCOLOR),line=dict(shape='spline', smoothing=1.3)), row=2, col=1)
    DTSR_fig.add_trace(go.Scatter(x=mainkpis["Date"], y=mainkpis["DWRSR"], mode="markers+lines", marker=dict(color=CHARTCOLOR),line=dict(shape='spline', smoothing=1.3)), row=3, col=1)
    DTSR_fig.add_trace(go.Scatter(x=mainkpis["Date"], y=mainkpis["DVCST"], mode="markers+lines", marker=dict(color=CHARTCOLOR),line=dict(shape='spline', smoothing=1.3)), row=4, col=1)
    DTSR_fig.add_trace(go.Scatter(x=mainkpis["Date"], y=mainkpis["DVQMOS"], mode="markers+lines", marker=dict(color=CHARTCOLOR),line=dict(shape='spline', smoothing=1.3)), row=5, col=1)
    DTSR_fig.add_trace(go.Scatter(x=mainkpis["Date"], y=mainkpis["DSSR"], mode="markers+lines", marker=dict(color=CHARTCOLOR),line=dict(shape='spline', smoothing=1.3)), row=6, col=1)
    DTSR_fig.update_layout(yaxis_title="Main KQIs", height=1000, font=dict(color="white", size=12), xaxis=dict(tickformat="%d", showgrid=False,tickfont=dict(color=CHARTCOLOR),zerolinecolor=CHARTCOLOR,showline=True, linecolor=CHARTCOLOR, linewidth=2), yaxis=dict(tickformat="%d", showgrid=False), showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=10, b=10))
    DTSR_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    DTSR_fig.update_xaxes(showgrid=False, zeroline=True,tickfont=dict(color=CHARTCOLOR),zerolinecolor=CHARTCOLOR,showline=False, linecolor=CHARTCOLOR, linewidth=0)  # Remove X-axis grids for all
    DTSR_fig.update_yaxes(showgrid=False, zeroline=True,tickfont=dict(color=CHARTCOLOR),zerolinecolor=CHARTCOLOR,showline=False, linecolor=CHARTCOLOR, linewidth=0)  # Remove Y-axis grids for all
    ##################################################### Scatter Chart ##################################################

    ################################################# Bar and Line Combo Chart ##############################################
    ## Daily Total Active Data Users Count and Traffic
    ################################################# Bar and Line Combo Chart ##############################################
    DTADUCT_fig = go.Figure()
    DTADUCT_fig = make_subplots(specs=[[{"secondary_y": True}]])
    DTADUCT_fig.add_trace(go.Scatter(x=mainkpis['Date'], y=mainkpis['DTADUC'], name="Active User Count", marker={'color':'lightblue'},mode="lines",line=dict(shape='spline', smoothing=1.3),text=mainkpis['DTADUC'],textposition="bottom center",textfont=dict( family="sans serif", size=13,color="black")),secondary_y=True)
    DTADUCT_fig.add_trace(go.Bar(x=mainkpis['Date'], y=mainkpis['DTADUT'], name="Traffic",text=mainkpis['DTADUT'],textposition="inside",marker={'color':'maroon'},textfont=dict(family="sans serif",size=13,color="white")),secondary_y=False)
    DTADUCT_fig.update_layout(title="Total Active Data Users Count and Traffic",title_x=0.5, font=dict(color="white", size=12),template='plotly_white', height=200, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=30, b=10))
    DTADUCT_fig.update_yaxes(title_text="Users Count", secondary_y=False,showgrid=False)
    DTADUCT_fig.update_yaxes(title_text="Traffic", secondary_y=True,showgrid=False)
    ################################################# Bar and Line Combo Chart ##############################################

    ################################################# Bar and Line Combo Chart ##############################################
    ## Daily Total Active Data Roamers Count and Traffic
    ################################################# Bar and Line Combo Chart ##############################################
    DTADRCT_fig = go.Figure()
    DTADRCT_fig = make_subplots(specs=[[{"secondary_y": True}]])
    DTADRCT_fig.add_trace(go.Scatter(x=mainkpis['Date'], y=mainkpis['DTADRC'], name="Active Data Roamers Count", marker={'color':'blue'},mode="lines",line=dict(shape='spline', smoothing=1.3),text=mainkpis['DTADRC'],textposition="bottom center",textfont=dict( family="sans serif", size=13,color="white")),secondary_y=True)
    DTADRCT_fig.add_trace(go.Bar(x=mainkpis['Date'], y=mainkpis['DTADRT'], name="Traffic",text=mainkpis['DTADRT'],textposition="inside",marker={'color':'slategrey'}, textfont=dict(family="sans serif",size=13,color="white")),secondary_y=False)
    DTADRCT_fig.update_layout(title="Total Active Data Roamers Count and Traffic", title_x=0.3, font=dict(color="white", size=12),template='plotly_white', height=200, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=30, b=10))
    DTADRCT_fig.update_yaxes(title_text="Roaming Users Count", secondary_y=False,showgrid=False)
    DTADRCT_fig.update_yaxes(title_text="Traffic", secondary_y=True,showgrid=False)
    ################################################# Bar and Line Combo Chart ##############################################

    ##################################################### Bar Chart ##################################################
    ## Top Device and Brands
    ##################################################### Bar Chart ##################################################
    TOPDVBR_fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]],subplot_titles=("Top Device Types", "Top Brands"))
    TOPDVBR_fig.add_trace(go.Bar(x=devtypes["Device"], y=devtypes["Share"],marker=dict(color=devtypes["Share"], colorscale='Blues')), row=1, col=1)
    TOPDVBR_fig.add_trace(go.Bar(x=topbrnds["Brand"], y=topbrnds["Share"],marker=dict(color=topbrnds["Share"], colorscale='Blues') ), row=1, col=2)
    TOPDVBR_fig.update_layout(font=dict(color="white", size=12), yaxis_title="Top Device Types and Brands", xaxis=dict(tickformat="%d", showgrid=False), yaxis=dict(tickformat="%d", showgrid=False), height=300, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=10, b=10))
    TOPDVBR_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    TOPDVBR_fig.update_xaxes(showgrid=False, zeroline=False)  # Remove X-axis grids for all
    TOPDVBR_fig.update_yaxes(showgrid=False, zeroline=False)  # Remove Y-axis grids for all
    ##################################################### Bar Chart ##################################################

    ##################################################### Horintal Bar Chart ##################################################
    ## Top OTT Apps and Countries
    ##################################################### Horintal Bar Chart ##################################################
    TOPOTCON_fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]],subplot_titles=("Top OTT Apps", "Top Countries"))
    TOPOTCON_fig.add_trace(go.Bar(y=topoapps["App"], x=topoapps["Share"],orientation="h", marker=dict(color=topoapps["Share"], colorscale='Tealrose')), row=1, col=1)
    TOPOTCON_fig.add_trace(go.Bar(y=topcntrs["Country"], x=topcntrs["Share"],orientation="h", marker=dict(color=topcntrs["Share"], colorscale='darkmint')), row=1, col=2)
    TOPOTCON_fig.update_layout(font=dict(color="white", size=12), yaxis_title="Top List", xaxis=dict(tickformat="%d", showgrid=False), yaxis=dict(tickformat="%d", showgrid=False), height=300, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=10, r=10, t=10, b=10))
    TOPOTCON_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    TOPOTCON_fig.update_xaxes(showgrid=False, zeroline=False)  # Remove X-axis grids for all
    TOPOTCON_fig.update_yaxes(showgrid=False, zeroline=False)  # Remove Y-axis grids for all
    ##################################################### Horintal Bar Chart ##################################################

    ################################################# Choropleth World Map ##############################################
    ## Top Countries by Roaming Users
    ################################################# Choropleth World Map ##############################################

    # Define a new column for color categories based on value ranges
    def categorize(value):
        if value > 10000:
            return "Very High (>10K)"
        elif value > 1000:
            return "High (>1K)"
        elif value > 100:
            return "Moderate (>100)"
        elif value > 10:
            return "Low (>10)"
        else:
            return "Very Low (≤10)"

    roagmaps["Color_Category"] = roagmaps["Roamers"].apply(categorize)

    # Define a custom discrete color scale
    custom_colors = {
        "Very High (>10K)": "darkgreen",
        "High (>1K)": "lightgreen",
        "Moderate (>100)": "yellow",
        "Low (>10)": "orange",
        "Very Low (≤10)": "white",
    }

    ROAMWMAP_fig = px.choropleth(roagmaps,locations="Code", color="Color_Category", color_discrete_map=custom_colors, hover_name="Country", projection="natural earth",center={"lat": 25, "lon": 10}, title="Visited Countries")
    ROAMWMAP_fig.update_layout(font=dict(color="white", size=10),height=500, showlegend=False, plot_bgcolor=DASHBBGCOL, paper_bgcolor=DASHBBGCOL,margin=dict(l=0, r=0, t=0, b=0), geo=dict(projection_scale=1.22))
    ROAMWMAP_fig.update_geos(bgcolor=DASHBBGCOL,lakecolor=DASHBBGCOL,showframe=False)
    ################################################# Choropleth World Map ##############################################

    return TOTDDATA_fig, MAINKQIS_fig, DTSR_fig, DTADUCT_fig, DTADRCT_fig, TOPDVBR_fig, TOPOTCON_fig, ROAMWMAP_fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
