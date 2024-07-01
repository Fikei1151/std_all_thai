import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests
import dash_bootstrap_components as dbc

# Load the data
df = pd.read_csv('graduates_m6_2566.csv')

# Mapping dictionary from Thai to English province names
province_mapping = {
    'กระบี่': 'Krabi',
    'กรุงเทพมหานคร': 'Bangkok Metropolis',
    'กาญจนบุรี': 'Kanchanaburi',
    'กาฬสินธุ์': 'Kalasin',
    'กำแพงเพชร': 'Kamphaeng Phet',
    'ขอนแก่น': 'Khon Kaen',
    'จันทบุรี': 'Chanthaburi',
    'ฉะเชิงเทรา': 'Chachoengsao',
    'ชลบุรี': 'Chon Buri',
    'ชัยนาท': 'Chai Nat',
    'ชัยภูมิ': 'Chaiyaphum',
    'ชุมพร': 'Chumphon',
    'ตรัง': 'Trang',
    'ตราด': 'Trat',
    'ตาก': 'Tak',
    'นครนายก': 'Nakhon Nayok',
    'นครปฐม': 'Nakhon Pathom',
    'นครพนม': 'Nakhon Phanom',
    'นครราชสีมา': 'Nakhon Ratchasima',
    'นครศรีธรรมราช': 'Nakhon Si Thammarat',
    'นครสวรรค์': 'Nakhon Sawan',
    'นนทบุรี': 'Nonthaburi',
    'นราธิวาส': 'Narathiwat',
    'น่าน': 'Nan',
    'บึงกาฬ': 'Bueng Kan',
    'บุรีรัมย์': 'Buri Ram',
    'ปทุมธานี': 'Pathum Thani',
    'ประจวบคีรีขันธ์': 'Prachuap Khiri Khan',
    'ปราจีนบุรี': 'Prachin Buri',
    'ปัตตานี': 'Pattani',
    'พระนครศรีอยุธยา': 'Phra Nakhon Si Ayutthaya',
    'พะเยา': 'Phayao',
    'พังงา': 'Phangnga',
    'พัทลุง': 'Phatthalung',
    'พิจิตร': 'Phichit',
    'พิษณุโลก': 'Phitsanulok',
    'ภูเก็ต': 'Phuket',
    'มหาสารคาม': 'Maha Sarakham',
    'มุกดาหาร': 'Mukdahan',
    'ยะลา': 'Yala',
    'ยโสธร': 'Yasothon',
    'ระนอง': 'Ranong',
    'ระยอง': 'Rayong',
    'ราชบุรี': 'Ratchaburi',
    'ร้อยเอ็ด': 'Roi Et',
    'ลพบุรี': 'Lop Buri',
    'ลำปาง': 'Lampang',
    'ลำพูน': 'Lamphun',
    'ศรีสะเกษ': 'Si Sa Ket',
    'สกลนคร': 'Sakon Nakhon',
    'สงขลา': 'Songkhla',
    'สตูล': 'Satun',
    'สมุทรปราการ': 'Samut Prakan',
    'สมุทรสงคราม': 'Samut Songkhram',
    'สมุทรสาคร': 'Samut Sakhon',
    'สระบุรี': 'Saraburi',
    'สระแก้ว': 'Sa Kaeo',
    'สิงห์บุรี': 'Sing Buri',
    'สุพรรณบุรี': 'Suphan Buri',
    'สุราษฎร์ธานี': 'Surat Thani',
    'สุรินทร์': 'Surin',
    'สุโขทัย': 'Sukhothai',
    'หนองคาย': 'Nong Khai',
    'หนองบัวลำภู': 'Nong Bua Lam Phu',
    'อำนาจเจริญ': 'Amnat Charoen',
    'อุดรธานี': 'Udon Thani',
    'อุตรดิตถ์': 'Uttaradit',
    'อุทัยธานี': 'Uthai Thani',
    'อุบลราชธานี': 'Ubon Ratchathani',
    'อ่างทอง': 'Ang Thong',
    'เชียงราย': 'Chiang Rai',
    'เชียงใหม่': 'Chiang Mai',
    'เพชรบุรี': 'Phetchaburi',
    'เพชรบูรณ์': 'Phetchabun',
    'เลย': 'Loei',
    'แพร่': 'Phrae',
    'แม่ฮ่องสอน': 'Mae Hong Son'
}

# Replace Thai province names with English names
df['schools_province'] = df['schools_province'].map(province_mapping)

# Add a column to highlight Narathiwat
df['highlight'] = df['schools_province'].apply(lambda x: 'highlight' if x == 'Narathiwat' else 'normal')

# Load the GeoJSON file for Thailand provinces
geojson_url = 'https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json'
geojson_data = requests.get(geojson_url).json()

# Create the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Create the choropleth map
def create_choropleth(theme):
    fig = px.choropleth(
        df,
        geojson=geojson_data,
        locations='schools_province',
        featureidkey='properties.name',
        color='totalstd',
        hover_name='schools_province',
        hover_data=['totalmale', 'totalfemale'],
        title='จำนวนนักเรียนที่จบการศึกษาระดับ ม.6 ปี 2567 แยกตามจังหวัด',
        labels={'totalstd': 'Total Students', 'totalmale': 'Total Male', 'totalfemale': 'Total Female'},
        template=theme,
        color_continuous_scale=px.colors.sequential.Blues
    )
    # Highlight Narathiwat
    fig.update_traces(marker_line_width=2)
    fig.add_choropleth(
        geojson=geojson_data,
        locations=['Narathiwat'],
        z=[1],
        featureidkey='properties.name',
        colorscale=[[0, 'red'], [1, 'red']],
        showscale=False,
        marker=dict(line=dict(width=2, color='darkred'))
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("จำนวนนักเรียนที่จบการศึกษาระดับ ม.6 ปี 2567 แยกตามจังหวัด"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="map", figure=create_choropleth('plotly_white')), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("เลือกจังหวัด:"),
            dcc.Dropdown(
                id='province-dropdown',
                options=[{'label': province, 'value': province} for province in df['schools_province'].unique()],
                value='Narathiwat',  # Default value to Narathiwat
                placeholder="เลือกจังหวัด"
            ),
            html.Div(id='province-info')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("โหมดสว่าง", id="light-mode-button", color="primary", className="me-2"),
            dbc.Button("โหมดมืด", id="dark-mode-button", color="secondary")
        ], width=12)
    ])
], fluid=True, id='body')

# Callback to update the map and theme
@app.callback(
    Output('map', 'figure'),
    Output('body', 'className'),
    [Input('light-mode-button', 'n_clicks'), Input('dark-mode-button', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_theme(light_clicks, dark_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'light-mode-button':
        theme = 'plotly_white'
        class_name = ''
    elif button_id == 'dark-mode-button':
        theme = 'plotly_dark'
        class_name = 'dark-mode'
    return create_choropleth(theme), class_name

# Callback to update province information
@app.callback(
    Output('province-info', 'children'),
    [Input('province-dropdown', 'value')]
)
def update_province_info(selected_province):
    if selected_province is None:
        return "กรุณาเลือกจังหวัด"
    province_data = df[df['schools_province'] == selected_province].iloc[0]
    return html.Div([
        html.H3(f"ข้อมูลจังหวัด: {selected_province}"),
        html.P(f"จำนวนนักเรียนทั้งหมด: {province_data['totalstd']}"),
        html.P(f"จำนวนนักเรียนชาย: {province_data['totalmale']}"),
        html.P(f"จำนวนนักเรียนหญิง: {province_data['totalfemale']}")
    ])

# Add CSS for dark mode
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body.dark-mode {
                background-color: black;
                color: white;
            }
            body.dark-mode .dash-graph {
                background-color: #333;
                color: white;
            }
        </style>
    </head>
    <body>
        <div id="body" class="{%class%}">
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </div>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
