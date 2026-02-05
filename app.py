# Import required libraries
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Import page modules
from pages import page1_executive, page2_countries, page3_products, page4_balance, page5_transport, page6_alerts, ai_chat

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "MTID - Merchandise Trade Intelligence Dashboard"

# Load the data
df_formal = pd.read_csv('data/formal_trade.csv')
df_informal = pd.read_csv('data/informal_trade.csv')

# Add a column to identify the trade type
df_formal['Trade_Type'] = 'Formal'
df_informal['Trade_Type'] = 'Informal'

# Combine for easier filtering
df = pd.concat([df_formal, df_informal], ignore_index=True)

# Sidebar Navigation
sidebar = html.Div([
    html.Div([
        html.H4("MTID", className="text-white text-center py-3"),
        html.Hr(className="bg-white"),
        
        # Trade Type Buttons
        html.Div([
            html.P("Select Trade Type:", className="text-white-50 small mb-2 px-3"),
            dbc.ButtonGroup([
                dbc.Button("Formal", id="btn-formal", color="light", size="sm", className="w-50"),
                dbc.Button("Informal", id="btn-informal", outline=True, color="light", size="sm", className="w-50"),
            ], className="w-100 px-3 mb-3")
        ]),
        
        html.Hr(className="bg-white"),
        
        # Page Navigation
        html.P("Navigation:", className="text-white-50 small mb-2 px-3"),
        dbc.Nav([
            dbc.NavLink("📊 Executive Overview", href="#", id="nav-page1", active=True, className="text-white"),
            dbc.NavLink("🌍 Partner Countries", href="#", id="nav-page2", className="text-white"),
            dbc.NavLink("📦 Product Analysis", href="#", id="nav-page3", className="text-white"),
            dbc.NavLink("⚖️ Trade Balance", href="#", id="nav-page4", className="text-white"),
            dbc.NavLink("🚢 Transport & Customs", href="#", id="nav-page5", className="text-white"),
            dbc.NavLink("🚨 Smart Alerts", href="#", id="nav-page6", className="text-white"),
            dbc.NavLink("📘 Metadata", href="#", id="nav-page7", className="text-white"),
        ], vertical=True, pills=True),
    ], style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '250px',
        'padding': '0',
        'background-color': '#2c3e50'
    })
], style={'width': '250px'})

# Main Content Area
content = html.Div(id='page-content', style={
    'margin-left': '250px',
    'padding': '20px'
})

# App Layout
app.layout = html.Div([
    # Hidden div to store current page and trade type
    html.Div(id='current-page', style={'display': 'none'}, children='page1'),
    html.Div(id='selected-trade-type', style={'display': 'none'}, children='Formal'),
    
    # Sidebar and Content
    sidebar,
    content,
    
    # AI Chat Component
    ai_chat.chat_interface()
])

# Callback: Update Trade Type Selection
@callback(
    Output('selected-trade-type', 'children'),
    Output('btn-formal', 'color'),
    Output('btn-formal', 'outline'),
    Output('btn-informal', 'color'),
    Output('btn-informal', 'outline'),
    Input('btn-formal', 'n_clicks'),
    Input('btn-informal', 'n_clicks')
)
def update_trade_type(formal_clicks, informal_clicks):
    """Update selected trade type and button styles"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'Formal', 'light', False, 'light', True
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'btn-formal':
        return 'Formal', 'light', False, 'light', True
    else:
        return 'Informal', 'light', True, 'light', False

# Callback: Update Active Page
@callback(
    Output('current-page', 'children'),
    Output('nav-page1', 'active'),
    Output('nav-page2', 'active'),
    Output('nav-page3', 'active'),
    Output('nav-page4', 'active'),
    Output('nav-page5', 'active'),
    Output('nav-page6', 'active'),
    Output('nav-page7', 'active'),
    Input('nav-page1', 'n_clicks'),
    Input('nav-page2', 'n_clicks'),
    Input('nav-page3', 'n_clicks'),
    Input('nav-page4', 'n_clicks'),
    Input('nav-page5', 'n_clicks'),
    Input('nav-page6', 'n_clicks'),
    Input('nav-page7', 'n_clicks'),
)
def update_page(n1, n2, n3, n4, n5, n6, n7):
    """Update current page and navigation highlighting"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return 'page1', True, False, False, False, False, False, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Map button to page
    page_map = {
        'nav-page1': ('page1', True, False, False, False, False, False, False),
        'nav-page2': ('page2', False, True, False, False, False, False, False),
        'nav-page3': ('page3', False, False, True, False, False, False, False),
        'nav-page4': ('page4', False, False, False, True, False, False, False),
        'nav-page5': ('page5', False, False, False, False, True, False, False),
        'nav-page6': ('page6', False, False, False, False, False, True, False),
        'nav-page7': ('page7', False, False, False, False, False, False, True),
    }
    
    return page_map.get(button_id, ('page1', True, False, False, False, False, False, False))

# Callback: Display Page Content
@callback(
    Output('page-content', 'children'),
    Input('current-page', 'children'),
    Input('selected-trade-type', 'children')
)
def display_page(page, trade_type):
    """Display the selected page content"""
    
    # Header for all pages
    header = dbc.Row([
        dbc.Col([
            html.H2("🌍 Merchandise Trade Intelligence Dashboard", className="text-primary mb-0"),
            html.P("National Institute of Statistics Rwanda (NISR)", className="text-muted")
        ], width=8),
        dbc.Col([
            html.P("Last Updated: January 2026", className="text-end text-muted mb-0"),
            html.P(f"Viewing: {trade_type.upper()} TRADE", className="text-end fw-bold")
        ], width=4)
    ], className="mb-4")
    
    if page == 'page1':
        return html.Div([
            header,
            html.Hr(),
            html.H3("📊 Page 1: Executive Trade Overview", className="mb-4"),
            page1_executive.layout(df)
        ])
    
    elif page == 'page2':
     return html.Div([
         header,
        html.Hr(),
        html.H3("🌍 Page 2: Trade by Partner Country", className="mb-4"),
        page2_countries.layout(df)
    ])
    
    elif page == 'page3':
     return html.Div([
        header,
        html.Hr(),
        html.H3("📦 Page 3: Product-Level Trade Analysis", className="mb-4"),
        page3_products.layout(df)
    ])
    
    elif page == 'page4':
     return html.Div([
        header,
        html.Hr(),
        html.H3("⚖️ Page 4: Trade Balance & Structure", className="mb-4"),
        page4_balance.layout(df)
    ])
    
    elif page == 'page5':
     return html.Div([
        header,
        html.Hr(),
        html.H3("🚢 Page 5: Transport Mode & Customs Insights", className="mb-4"),
        page5_transport.layout(df)
    ])
    
    elif page == 'page6':
     return html.Div([
        header,
        html.Hr(),
        html.H3("🚨 Page 6: Smart Alerts - Data Validation Support", className="mb-4"),
        page6_alerts.layout(df)
    ])
    
    elif page == 'page7':
     return html.Div([
        header,
        html.Hr(),
        html.H3("📘 Page 7: Metadata, Methodology & Raw Data", className="mb-4"),
        
        # Metadata Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📋 Metadata & Data Source", className="mb-0")),
                    dbc.CardBody([
                        html.H6("Data Source", className="text-primary mb-2"),
                        html.P("EUROTRACE / ASYCUDA++ / Rwanda Revenue Authority (RRA)", className="mb-3"),
                        
                        html.H6("Scope", className="text-primary mb-2"),
                        html.P("Formal and Informal Merchandise Trade", className="mb-3"),
                        
                        html.H6("Coverage", className="text-primary mb-2"),
                        html.P("All merchandise goods crossing Rwanda's borders (imports and exports)", className="mb-3"),
                        
                        html.H6("Exclusions", className="text-primary mb-2"),
                        html.P("Trade in services, informal cross-border trade not captured by customs", className="mb-3"),
                        
                        html.H6("Publication Frequency", className="text-primary mb-2"),
                        html.P("Quarterly, with annual aggregations", className="mb-3"),
                        
                        html.H6("Classification System", className="text-primary mb-2"),
                        html.P("Harmonized System (HS) - International standard for classifying traded products", className="mb-3"),
                        
                        html.H6("Currency", className="text-primary mb-2"),
                        html.P("All values reported in United States Dollars (USD)", className="mb-0"),
                    ])
                ], className="shadow-sm mb-4")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🔬 Methodology", className="mb-0")),
                    dbc.CardBody([
                        html.H6("Data Collection", className="text-primary mb-2"),
                        html.P("Data is collected at customs border posts using ASYCUDA++ system", className="mb-3"),
                        
                        html.H6("Valuation Method", className="text-primary mb-2"),
                        html.P("FOB (Free on Board) for exports, CIF (Cost, Insurance, Freight) for imports", className="mb-3"),
                        
                        html.H6("Data Quality Control", className="text-primary mb-2"),
                        html.Ul([
                            html.Li("Automated validation checks in ASYCUDA++"),
                            html.Li("Manual review by customs officers"),
                            html.Li("Statistical validation by NISR analysts"),
                            html.Li("Cross-verification with partner country data (mirror statistics)")
                        ], className="mb-3"),
                        
                        html.H6("Confidentiality", className="text-primary mb-2"),
                        html.P("Individual trader information is protected. Only aggregated statistics are published.", className="mb-3"),
                        
                        html.H6("Contact Information", className="text-primary mb-2"),
                        html.P([
                            "National Institute of Statistics of Rwanda (NISR)",
                            html.Br(),
                            "Email: info@statistics.gov.rw",
                            html.Br(),
                            "Website: www.statistics.gov.rw"
                        ], className="mb-0"),
                    ])
                ], className="shadow-sm mb-4")
            ], width=6),
        ]),
        
        html.Hr(),
        
        # Raw Dataset Section
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardHeader(html.H5("📊 Raw Dataset Viewer", className="mb-0")),
            dbc.CardBody([
                html.P([
                    "This is the complete raw dataset used throughout the dashboard. ",
                    "The dataset shown matches your current trade type selection (Formal/Informal) from the sidebar buttons. ",
                    "You can search, filter, sort, and export the data to Excel using the button in the top-right of the table."
                ], className="text-muted mb-3"),
                
                html.P([
                    html.Strong("💡 Tip: "),
                    "Use the filter boxes below each column header to search for specific values. ",
                    "Click column headers to sort. Click the 'Export' button to download as Excel."
                ], className="text-info small mb-3"),
                
                # Dataset Info
                html.Div(id='p7-dataset-info', className="mb-3"),
                
                # Data Table
                html.Div(id='p7-raw-data-table')
            ])
        ], className="shadow-sm")
    ], width=12)
]),
        
        html.Hr(),
        
        # Data Dictionary
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📖 Data Dictionary", className="mb-0")),
                    dbc.CardBody([
                        html.P("Explanation of all columns in the dataset:", className="fw-bold mb-3"),
                        
                        html.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Column Name", style={'width': '20%'}),
                                    html.Th("Type", style={'width': '15%'}),
                                    html.Th("Description", style={'width': '65%'})
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([html.Td("Year"), html.Td("Numeric"), html.Td("Calendar year of the trade transaction")]),
                                html.Tr([html.Td("Quarter"), html.Td("Text"), html.Td("Quarter of the year (Q1, Q2, Q3, Q4)")]),
                                html.Tr([html.Td("Month"), html.Td("Text"), html.Td("Month when the trade occurred")]),
                                html.Tr([html.Td("Flow"), html.Td("Categorical"), html.Td("Direction of trade: Export or Import")]),
                                html.Tr([html.Td("HS2"), html.Td("Text"), html.Td("2-digit Harmonized System code (broad product category)")]),
                                html.Tr([html.Td("HS4"), html.Td("Text"), html.Td("4-digit Harmonized System code (product sub-category)")]),
                                html.Tr([html.Td("HS_Code"), html.Td("Text"), html.Td("6-digit Harmonized System code (detailed product)")]),
                                html.Tr([html.Td("HS_Description"), html.Td("Text"), html.Td("Description of the product")]),
                                html.Tr([html.Td("Partner_Country"), html.Td("Text"), html.Td("Destination country (exports) or origin country (imports)")]),
                                html.Tr([html.Td("Region"), html.Td("Text"), html.Td("Geographic/economic region of partner country")]),
                                html.Tr([html.Td("Trade_Value_USD"), html.Td("Numeric"), html.Td("Monetary value of trade in US Dollars")]),
                                html.Tr([html.Td("Quantity"), html.Td("Numeric"), html.Td("Physical quantity of goods traded")]),
                                html.Tr([html.Td("Unit"), html.Td("Text"), html.Td("Measurement unit for quantity (Kg, Tonnes, Units, etc.)")]),
                                html.Tr([html.Td("Mode_of_Transport"), html.Td("Text"), html.Td("How goods were transported (Road, Air, Sea)")]),
                                html.Tr([html.Td("Customs_Office"), html.Td("Text"), html.Td("Border post where trade was recorded")]),
                            ])
                        ], className="table table-striped table-hover")
                    ])
                ], className="shadow-sm")
            ], width=12)
        ]),
    ])
    
    return html.Div([header, html.P("Page not found")])

# Register Page 1 callbacks
page1_executive.register_callbacks(app, df)

# Register Page 2 callbacks
page2_countries.register_callbacks(app, df)
# Register Page 3 callbacks
page3_products.register_callbacks(app, df)
# Register Page 4 callbacks
page4_balance.register_callbacks(app, df)
# Register Page 5 callbacks
page5_transport.register_callbacks(app, df)
# Register Page 6 callbacks
page6_alerts.register_callbacks(app, df)
# Register AI Chat callbacks
ai_chat.register_callbacks(app, df)
# Page 7: Raw Dataset Viewer Callbacks
@callback(
    Output('p7-dataset-info', 'children'),
    Output('p7-raw-data-table', 'children'),
    Input('selected-trade-type', 'children')
)
def update_raw_dataset(trade_type):
    """Update raw dataset view based on selected trade type"""
    
    try:
        # Filter data by trade type
        display_df = df[df['Trade_Type'] == trade_type].copy()
        
        # Remove Trade_Type column from display
        if 'Trade_Type' in display_df.columns:
            display_df = display_df.drop('Trade_Type', axis=1)
        
        # Check if we have data
        if len(display_df) == 0:
            return (
                dbc.Alert("No data available for this trade type.", color="warning"),
                html.P("Please check your data files.")
            )
        
        # Dataset info
        dataset_info = dbc.Alert([
            html.Strong(f"Currently viewing: {trade_type} Trade Dataset"),
            html.Br(),
            f"📊 Total Records: {len(display_df):,} | ",
            f"📋 Columns: {len(display_df.columns)} | ",
            f"📅 Years: {', '.join(map(str, sorted(display_df['Year'].unique())))} | ",
            f"📆 Quarters: {', '.join(sorted(display_df['Quarter'].unique()))}"
        ], color="primary" if trade_type == "Formal" else "success")
        
        # Create interactive data table
        data_table = dash_table.DataTable(
            id='raw-data-table-display',
            data=display_df.to_dict('records'),
            columns=[{'name': col, 'id': col, 'deletable': False} for col in display_df.columns],
            
            # Styling
            style_table={
                'overflowX': 'auto',
                'maxHeight': '600px',
                'overflowY': 'auto'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '12px',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '13px',
                'minWidth': '120px',
                'maxWidth': '300px',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'left',
                'border': '1px solid #ddd'
            },
            style_data={
                'border': '1px solid #ddd'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                },
                {
                    'if': {'column_id': 'Trade_Value_USD'},
                    'fontWeight': 'bold',
                    'color': '#007bff'
                },
                {
                    'if': {'column_id': 'Flow', 'filter_query': '{Flow} = "Export"'},
                    'color': '#28a745'
                },
                {
                    'if': {'column_id': 'Flow', 'filter_query': '{Flow} = "Import"'},
                    'color': '#dc3545'
                }
            ],
            
            # Features
            page_size=20,
            page_action='native',
            page_current=0,
            
            sort_action='native',
            sort_mode='multi',
            
            filter_action='native',
            
            # Export functionality
            export_format='xlsx',
            export_headers='display',
            
            # Column resizing
            style_cell_conditional=[
                {'if': {'column_id': 'Year'}, 'width': '80px'},
                {'if': {'column_id': 'Quarter'}, 'width': '80px'},
                {'if': {'column_id': 'Month'}, 'width': '80px'},
                {'if': {'column_id': 'Flow'}, 'width': '90px'},
                {'if': {'column_id': 'HS2'}, 'width': '80px'},
                {'if': {'column_id': 'HS4'}, 'width': '90px'},
                {'if': {'column_id': 'HS_Code'}, 'width': '100px'},
                {'if': {'column_id': 'HS_Description'}, 'width': '250px'},
                {'if': {'column_id': 'Partner_Country'}, 'width': '150px'},
                {'if': {'column_id': 'Region'}, 'width': '120px'},
                {'if': {'column_id': 'Trade_Value_USD'}, 'width': '150px'},
                {'if': {'column_id': 'Quantity'}, 'width': '120px'},
                {'if': {'column_id': 'Unit'}, 'width': '100px'},
                {'if': {'column_id': 'Mode_of_Transport'}, 'width': '150px'},
                {'if': {'column_id': 'Customs_Office'}, 'width': '150px'},
            ],
            
            # Tooltips
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in display_df.to_dict('records')
            ],
            tooltip_duration=None
        )
        
        return dataset_info, data_table
    
    except Exception as e:
        error_msg = dbc.Alert([
            html.H5("❌ Error Loading Dataset", className="alert-heading"),
            html.P(f"Error: {str(e)}")
        ], color="danger")
        
        return error_msg, html.P("Unable to load data table.")
# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)