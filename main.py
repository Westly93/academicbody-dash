import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, dash_table, no_update, State
from dash.dependencies import Output, Input
import plotly.express as px


def load_dataframe():
    data = pd.read_csv("./data/new_data.csv")
    data = data.drop(columns=['mark.1', 'id'])
    data = data.drop_duplicates(['regnum', 'module'], keep='last')
    data['gender'] = data['gender'].replace(
        {'female': 'Female', 'male': 'Male'})
    return data


data = load_dataframe()
# list all unique faculties
faculties = data.faculty.unique().tolist()
programmes = data[data['faculty'] == faculties[0]].programme.unique().tolist()

# create a faculty select box
faculty = dcc.Dropdown(
    id="faculty_selection", options=faculties, value=faculties[0], clearable=False)
programme = dcc.Dropdown(id='programme_selection',
                         options=programmes, value=programmes[0])

# faculty infomation cards


def faculty_decision_distribution(faculty=faculties[0]):
    df = data[data['faculty'] == faculty]
    grouped_data = df.groupby(by="decision")['regnum'].nunique()
    grouped_data = grouped_data.reset_index(
        name="Students")
    fig = px.bar(
        grouped_data,
        x="decision",
        y="Students",
        # orientation='h',
        title="Decision Distribution of Student Population",
        color_discrete_sequence=["#0083B8"] * len(grouped_data),
        template="plotly_white"

    )
    fig.update_layout(height=300, width=300, showlegend=False,
                      template='simple_white')
    return fig

# selectible datatables


def dash_datatable():

    datatable = dash_table.DataTable(
        data[data['faculty'] == faculty].to_dict('records'),
        columns=[{"name": i, "id": i} for i in data.columns[:-2]],
        row_selectable='single',
        cell_selectable=True,
        style_data_conditional=[
            {
                "if": {
                    "state": "active"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
            {
                "if": {
                    "state": "selected"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            }

        ],
        id='tbl'),
    return datatable


# statistical cards


def faculty_cards(faculty=faculties[0]):
    decisions = data[data['faculty'] == faculty].decision.unique().tolist()
    cards = []
    for decision in decisions:
        new_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6([html.I(className="me-2"),
                            f"{decision}"], className="text-nowrap"),
                    html.I(className='fa-solid fa-users me-2'),
                    html.Span(
                        f"{data[(data['decision']== decision) & (data['faculty']== faculty)].regnum.nunique()}", className=""),
                ], className="border-start border-success border-5"
            ),
            className=""
        )
        cards.append(dbc.Col(new_card))
    cards_list = dbc.Container(
        dbc.Row(
            cards,
        ),
        fluid=True,
    )
    return cards_list


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.FONT_AWESOME],
)


sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Academic Body",
                        style={"color": "white"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"),
                     html.Span("Dashboard")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Projects"),
                    ],
                    href="/projects",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-envelope-open-text me-2"),
                        html.Span("Datasets"),
                    ],
                    href="/datasets",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

app.layout = html.Div(
    [
        sidebar,
        html.Div(
            [
                dash.page_container,
                html.H1('ACADEMIC BODY RESULTS PRESENTATION', style={
                        'text-align': 'center'}),
            ],
            className="content",
        ),
        html.Div(
            [
                faculty,
                html.Br(),
                dbc.Container(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="gender_distribution"),
                            ),
                            dbc.Col(dcc.Graph(id="graph"),
                                    ),
                            dbc.Col([
                                dbc.Button('🡠', id='back-button', outline=True, size="sm",
                                           className='mt-2 ml-2 col-1 mb-1', style={'display': 'none'}),
                                dbc.Row(
                                    dcc.Graph(id="decision_distribution"),
                                    justify='center'
                                )
                            ])
                        ]
                    ),
                    fluid=True,
                ),
                html.Br(),
                # faculty_cards(),
                # html.Br(),
                programme,
                html.Br(),
                dbc.Container(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="module_pass_rate"),
                            ),
                            dbc.Col(
                                dcc.Graph(id="attendance_type_distribution"),
                            ),
                            dbc.Col(
                                dcc.Graph(id="academicyear_distribution"),
                            )
                        ]
                    ),
                    fluid=True,
                ),
                dbc.Container(
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(id="attendance_type", clearable=False)
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="academic_year", clearable=False)
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="semester", clearable=False)
                        ),
                    ])
                ),
                html.Br(),
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('🡠', id='back-btn', outline=True, size="sm",
                                       className='mt-2 ml-2 col-1 mb-1', style={'display': 'none'}),
                            dbc.Row(
                                dcc.Graph(
                                    id="programme_decision_distribution"),
                                justify='center'
                            )

                        ]),
                    ]),
                    dbc.Row(
                        dbc.Col([
                            html.Div(id="decision_table")
                        ]),
                        justify='center'
                    )
                ]),


            ],

            className='content'
        ),
        html.Br(),
    ]
)


# callbacks
@app.callback(
    output=[Output('programme_selection', 'options'),
            Output('programme_selection', 'value')],
    inputs=[Input('faculty_selection', 'value')])
def update_programme(value):
    options = data[data['faculty'] == value].programme.unique().tolist()
    value = options[0]
    return options, value

# attendance types


@app.callback(
    output=[Output('attendance_type', 'options'),
            Output('attendance_type', 'value')],
    inputs=[Input('faculty_selection', 'value'), Input('programme_selection', 'value')])
def update_attendance_type(faculty, programme):
    options = data[(data['faculty'] == faculty) & (
        data['programme'] == programme)].attendancetype.unique().tolist()
    value = options[0]
    return options, value
# Academic year


@app.callback(
    output=[Output('academic_year', 'options'),
            Output('academic_year', 'value')],
    inputs=[Input('faculty_selection', 'value'), Input('programme_selection', 'value'), Input('attendance_type', 'value')])
def update_attendance_type(faculty, programme, attendance_type):
    options = data[(data['faculty'] == faculty) & (
        data['programme'] == programme) & (data['attendancetype'] == attendance_type)].academicyear.unique().tolist()
    value = options[0]
    return options, value
# semester


@app.callback(
    output=[Output('semester', 'options'),
            Output('semester', 'value')],
    inputs=[Input('faculty_selection', 'value'), Input('programme_selection', 'value'), Input('attendance_type', 'value')])
def update_attendance_type(faculty, programme, attendance_type):
    options = data[(data['faculty'] == faculty) & (
        data['programme'] == programme) & (data['attendancetype'] == attendance_type)].semester.unique().tolist()
    value = options[0]
    return options, value
# programme


@app.callback(
    Output("graph", "figure"),
    Input("faculty_selection", "value"))
def generate_chart(faculty):
    data_grouped = data[(data['faculty'] == faculty) & (data['decision'] == "PASS")].groupby(by="grade")[
        'regnum'].nunique()
    data_grouped = data_grouped.reset_index(
        name="Students")
    fig = px.pie(data_grouped, values='Students', names='grade', hole=0.3,
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 title=f"<b>Grade Distribution({data[(data['faculty']==faculty) & (data['decision'] == 'PASS')].regnum.nunique()})<b>"
                 )
    fig.update_layout(height=300, width=300, showlegend=False,
                      template='simple_white')
    return fig


# distribution by decision


""" @app.callback(
    Output("decision_distribution", "figure"),
    Input("faculty_selection", "value"))
def decision_distribution(faculty):
    data_grouped = data[(data['faculty'] == faculty) & (data['decision'] != "PASS")].groupby(by="decision")[
        'regnum'].nunique()
    data_grouped = data_grouped.reset_index(
        name="Students")
    fig = px.pie(data_grouped, values='Students', names='decision',
                 title=f"<b>Decision Distribution({data[(data['faculty']== faculty) & data['decision'] != 'PASS'].regnum.nunique()})<b>",
                 hole=0.3,
                 color_discrete_sequence=px.colors.sequential.YlOrRd_r)
    fig.update_layout(height=300, width=300,
                      showlegend=False, template='simple_white')
    return fig """

# gender distribution for the graduating students


@app.callback(
    Output("gender_distribution", "figure"),
    Input("faculty_selection", "value"))
def gender_distribution(faculty):
    data_grouped = data[(data['faculty'] == faculty) & (data['decision'] == "PASS")].groupby(by="gender")[
        'regnum'].nunique()
    data_grouped = data_grouped.reset_index(
        name="Students")
    fig = px.pie(data_grouped, values='Students', names='gender',
                 title=f"<b>Gender Distribution({data[(data['faculty']== faculty) & (data['decision']== 'PASS')].regnum.nunique()})<b>",
                 hole=0.3,
                 color_discrete_sequence=px.colors.sequential.YlOrRd_r)
    fig.update_layout(height=300, width=300,
                      showlegend=False, template='simple_white')
    return fig
# programme decision distribution


""" @app.callback(
    Output("programme_decision_distribution", "figure"),
    [Input("faculty_selection", "value"),
     Input("programme_selection", "value"),
     Input("attendance_type", "value"),
     Input("academic_year", "value"),
     Input("semester", "value")]
)
def programme_decision_distribution(faculty, programme, attendance_type, academic_year, semester):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme) & (data['attendancetype']
                                                                                 == attendance_type) & (data['academicyear'] == academic_year) & (data['semester'] == semester)]
    data_grouped = df.groupby(by="decision")[
        'regnum'].nunique().reset_index(name="Students")
    fig = px.pie(data_grouped, values='Students', names='decision',
                 hole=0.3,
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 title=f"<b>Decision Distribution {df.regnum.nunique()}</b>")
    fig.update_layout(height=300, width=300, showlegend=False,
                      template='simple_white')
    return fig """

# module passrate based on the Programe


@app.callback(
    Output("module_pass_rate", "figure"),
    [Input("faculty_selection", "value"),
     Input("programme_selection", "value")]
)
def module_pass_rate(faculty, programme):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme)]
    module_pass_rate = df.groupby(
        'module')['mark'].apply(lambda x: (x >= 50).mean() * 100).sort_values(ascending=False)
    module_pass_rate = module_pass_rate.reset_index(
        name="Pass Rate")
    fig = px.bar(
        module_pass_rate[:20],
        x="module",
        y="Pass Rate",
        # orientation='h',
        title=f"<b> Pass Rates by Module<b>",
        color_discrete_sequence=px.colors.sequential.YlGn_r,
    )

    fig.update_layout(height=300, width=400,
                      showlegend=False, template='simple_white')
    fig.update_xaxes(tickangle=45)
    return fig

# Attendance Type distribution


@app.callback(
    Output("attendance_type_distribution", "figure"),
    [Input("faculty_selection", "value"),
     Input("programme_selection", "value")]
)
def attendance_type_distribution(faculty, programme):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme)]
    data_grouped = df.groupby(by="attendancetype")[
        'regnum'].nunique().reset_index(name="Students")
    fig = px.pie(data_grouped, values='Students', names='attendancetype',
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r,
                 hole=.3,
                 title=f"<b>Attendance Type Distribution</b>")
    fig.update_layout(height=300, width=300,
                      showlegend=False, template='simple_white')
    return fig
# level distribution


@app.callback(
    Output("academicyear_distribution", "figure"),
    [Input("faculty_selection", "value"),
     Input("programme_selection", "value")]
)
def academicyear_distribution(faculty, programme):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme)]
    data_grouped = df.groupby(by="academicyear")[
        'regnum'].nunique().reset_index(name="Students")
    fig = px.pie(data_grouped, values='Students', names='academicyear',
                 hole=.3,
                 color_discrete_sequence=px.colors.sequential.YlOrRd_r,
                 title=f"<b>Academic Year Distribution</b>")
    fig.update_layout(height=300, width=300,
                      showlegend=False, template='simple_white')
    return fig
# display decisions


""" @app.callback(
    Output("decision_list", "children"),
    [Input("faculty_selection", "value"),
     Input("programme_selection", "value"),
     Input("attendance_type", "value"),
     Input("academic_year", "value"),
     Input("semester", "value")]
) 
def decision_list(faculty, programme, attendance_type, academic_year, semester):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme) & (data['attendancetype']
                                                                                 == attendance_type) & (data['academicyear'] == academic_year) & (data['semester'] == semester)]
    df = df.drop_duplicates(['regnum'], keep='last')
    df.drop(['mark', 'grade', 'faculty', 'programme', 'programmetype',
            'attendancetype', 'module', 'programmestatus'], axis=1, inplace=True)
    children = []
    for decision in df.decision.unique().tolist():
        child = html.Div([
            html.H6(
                f"{decision}({df[df['decision']==decision].regnum.nunique()})"),
            dash_table.DataTable(
                df[df['decision'] == decision].to_dict('records'),
                page_size=5,
                columns=[{"name": i, "id": i} for i in df.columns[:-2]],
                row_selectable='single',
                cell_selectable=True,
                style_data_conditional=[
                    {
                        "if": {
                            "state": "active"  # 'active' | 'selected'
                        },
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    },
                    {
                        "if": {
                            "state": "selected"  # 'active' | 'selected'
                        },
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    }

                ],
                id=f'tbl_{decision}'),
        ])
        children.append(html.Br())
        children.append(child)

    return children """

# drillthrough  callback


@app.callback(
    Output('decision_table', 'children'),  # to hide/unhide the back button
    [Input('programme_decision_distribution', 'clickData'),  # for getting the vendor name from graph
     Input("faculty_selection", "value"),
     Input("programme_selection", "value"),
     Input("attendance_type", "value"),
     Input("academic_year", "value"),
     Input("semester", "value")]
)
def drilldown(click_data, faculty, programme, attendancetype, academicyear, semester):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme) & (data['attendancetype']
                                                                                 == attendancetype) & (data['academicyear'] == academicyear) & (data['semester'] == semester)]
    df = df.drop_duplicates(['regnum'], keep='last')
    df.drop(['mark', 'grade', 'faculty', 'programme', 'programmetype',
            'attendancetype', 'module', 'programmestatus'], axis=1, inplace=True)
    df['id'] = df.regnum
    decisions = df.decision.unique().tolist()
    # using callback context to check which input was fired
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    children = []

    if trigger_id == 'programme_decision_distribution':
        # get vendor name from clickData
        if click_data is not None:
            decision = click_data['points'][0]['label']

            if decision in df.decision.unique():
                children.append(html.H6(
                    f"{decision}({df[df['decision']==decision].regnum.nunique()})"))
                children.append(dash_table.DataTable(
                    df[df['decision'] == decision].to_dict('records'),
                    page_size=5,
                    columns=[{"name": i, "id": i}
                             for i in df.columns[:-2]],
                    row_selectable='single',
                    cell_selectable=True,
                    style_data_conditional=[
                        {
                            "if": {
                                "state": "active"  # 'active' | 'selected'
                            },
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            "border": "1px solid rgb(0, 116, 217)",
                        },
                        {
                            "if": {
                                "state": "selected"  # 'active' | 'selected'
                            },
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            "border": "1px solid rgb(0, 116, 217)",
                        }

                    ],
                    id='tbl'))
                children.append(dbc.Modal(
                    [
                        dbc.ModalHeader("Selected Row"),
                        dbc.ModalBody(id="modal_body"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close_modal",
                                       className="ml-auto", n_clicks=0, size='sm')
                        ),
                    ],
                    id="modal",
                    size="lg",
                ))

                # returning the fig and unhiding the back button
                return children
            else:
                children.append(html.H6(
                    f"{decision}({df[df['decision']==decisions[0]].regnum.nunique()})"))
                children.append(dash_table.DataTable(
                    df[df['decision'] == decisions[0]].to_dict('records'),
                    page_size=5,
                    columns=[{"name": i, "id": i}
                             for i in df.columns[:-2]],
                    row_selectable='single',
                    cell_selectable=True,
                    style_data_conditional=[
                        {
                            "if": {
                                "state": "active"  # 'active' | 'selected'
                            },
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            "border": "1px solid rgb(0, 116, 217)",
                        },
                        {
                            "if": {
                                "state": "selected"  # 'active' | 'selected'
                            },
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            "border": "1px solid rgb(0, 116, 217)",
                        }

                    ],
                    id=f'tbl'))
                children.append(dbc.Modal(
                    [
                        dbc.ModalHeader("Student Information"),
                        dbc.ModalBody(id="modal_body"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close_modal",
                                       className="ml-auto", n_clicks=0)
                        ),
                    ],
                    id="modal",
                    size="lg",
                ))
                return children
        else:
            children.append(html.H6(
                f"{decision}({df[df['decision']==decisions[0]].regnum.nunique()})"))
            children.append(dash_table.DataTable(
                df[df['decision'] == decisions[0]].to_dict('records'),
                page_size=5,
                columns=[{"name": i, "id": i}
                         for i in df.columns[:-2]],
                row_selectable='single',
                cell_selectable=True,
                style_data_conditional=[
                    {
                        "if": {"state": "active"},  # 'active' | 'selected'
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    },
                    {
                        "if": {"state": "selected"},  # 'active' | 'selected'
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid rgb(0, 116, 217)",
                    }
                ],
                id='tbl'))
            children.append(dbc.Modal(
                [
                    dbc.ModalHeader("Selected Row"),
                    dbc.ModalBody(id="modal_body"),
                    dbc.ModalFooter(
                            dbc.Button("Close", id="close_modal",
                                       className="ml-auto", n_clicks=0)
                            ),
                ],
                id="modal",
                size="lg",
            ))
            return children

# open modal callback


@app.callback(
    (
        Output('tbl', 'selected_rows'),
    ),
    Input('tbl', 'active_cell'),
    prevent_initial_call=True
)
def update_graphs(active_cell):
    return (
        [active_cell['row']],
    ) if active_cell else ([],)


@app.callback(
    (
        Output('tbl', 'style_data_conditional'),
        Output('tbl', 'active_cell'),
        Output('tbl', 'selected_cells'),
        Output('modal', 'is_open'),
        Output('modal_body', 'children')
    ),
    [
        Input('tbl', 'derived_viewport_selected_row_ids'),
        Input('close_modal', 'n_clicks')
    ],
    [
        State('tbl', 'derived_viewport_selected_rows'),
        State('tbl', 'active_cell'),
        State('tbl', 'selected_cells'),
        State('modal', 'is_open')
    ],
    prevent_initial_call=True
)
def update_graphs2(selected_row_ids, close_modal_clicks, selected_rows, active_cell, selected_cells, is_modal_open):
    if selected_row_ids:
        if active_cell:
            active_cell['row'] = selected_rows[0]
        else:
            active_cell = no_update

        student_info = data[data['regnum'] == selected_row_ids[0]]
        modal_body = dbc.Container([
            dbc.Row([
                dbc.Col(html.P("Registration Number"),),
                dbc.Col(html.P(student_info['regnum'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("First Name"),),
                dbc.Col(html.P(student_info['firstnames'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Surname"),),
                dbc.Col(html.P(student_info['surname'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Programme"),),
                dbc.Col(html.P(student_info['programmecode'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Decision"),),
                dbc.Col(html.P(student_info['decision'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Attendance Type"),),
                dbc.Col(html.P(student_info['attendancetype'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Semester"),),
                dbc.Col(html.P(student_info['semester'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Academic Year"),),
                dbc.Col(html.P(student_info['academicyear'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Programme Type"),),
                dbc.Col(html.P(student_info['programmetype'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Col(html.P("Programme Status"),),
                dbc.Col(html.P(student_info['programmestatus'].iloc[0]))
            ]),
            dbc.Row([
                dbc.Label('Modules'),
                dash_table.DataTable(
                    student_info.drop(["programmetype", 'attendancetype', "academicyear", "semester", "decision",
                                      "firstnames", "surname", "faculty", "programme", "programmecode", "programmestatus"], axis=1).to_dict('records'),
                    columns=[{"name": i, "id": i}
                             for i in student_info.drop(["programmetype", 'attendancetype', "academicyear", "semester", "decision",
                                                         "firstnames", "surname", "faculty", "programme", "programmecode", "programmestatus"], axis=1).columns[:-2]],
                    style_data_conditional=[
                        {
                            "if": {"state": "active"},  # 'active' | 'selected'
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            "border": "1px solid rgb(0, 116, 217)",
                        },
                        {
                            # 'active' | 'selected'
                            "if": {"state": "selected"},
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            "border": "1px solid rgb(0, 116, 217)",
                        }
                    ],
                    id='data_tbl'
                ),
            ]),



        ])

        # html.P(f"Selected Row ID: {selected_row_ids}")
        is_modal_open = True

        return (
            [
                {
                    "if": {"filter_query": "{{id}} = '{}'".format(i)},
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                } for i in selected_row_ids
            ] + [
                {
                    "if": {"state": "active"},  # 'active' | 'selected'
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                }
            ],
            active_cell,
            [],
            is_modal_open,
            modal_body
        )
    elif close_modal_clicks:
        is_modal_open = False
        return ([], no_update, [], is_modal_open, no_update)
    else:
        return ([], no_update, [], is_modal_open, no_update)

# Faculty decision drill through


@app.callback(
    Output('decision_distribution', 'figure'),
    Output('back-button', 'style'),  # to hide/unhide the back button
    # for getting the vendor name from graph
    Input('decision_distribution', 'clickData'),
    Input('back-button', 'n_clicks'),
    Input('faculty_selection', 'value')
)
def decision_drilldown(click_data, n_clicks, faculty):

    # using callback context to check which input was fired
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    df = data[data['faculty'] == faculty]

    if trigger_id == 'decision_distribution':

        # get vendor name from clickData
        if click_data is not None:
            decision = click_data['points'][0]['label']

            if decision in df.decision.unique():
                # creating df for clicked vendor

                grouped_data = df[df['decision'] == decision].groupby(
                    by='programmecode')['regnum'].nunique().sort_values(ascending=False).reset_index(name="Students")

                # generating product sales bar graph
                fig = px.bar(grouped_data[:10], x='programmecode',
                             y='Students', color='programmecode')
                fig.update_layout(title=f'<b>Student Distribution({decision})<b>',
                                  height=300, width=300,
                                  showlegend=False, template='simple_white')
                fig.update_xaxes(tickangle=45)
                # returning the fig and unhiding the back button
                return fig, {'display': 'block'}

            else:
                data_grouped = data[(data['faculty'] == faculty)].groupby(by="decision")[
                    'regnum'].nunique()
                data_grouped = data_grouped.reset_index(
                    name="Students")
                fig = px.pie(data_grouped, values='Students', names='decision',
                             title=f"<b>Decision Distribution({data[data['faculty']== faculty].regnum.nunique()})<b>",
                             hole=0.3,
                             color_discrete_sequence=px.colors.sequential.YlOrRd_r)
                fig.update_layout(height=300, width=300,
                                  showlegend=False, template='simple_white')
                return fig, {'display': 'none'}  # hiding the back button

    else:
        data_grouped = data[(data['faculty'] == faculty)].groupby(by="decision")[
            'regnum'].nunique()
        data_grouped = data_grouped.reset_index(
            name="Students")
        fig = px.pie(data_grouped, values='Students', names='decision',
                     title=f"<b>Decision Distribution({data[(data['faculty']== faculty) & data['decision'] != 'PASS'].regnum.nunique()})<b>",
                     hole=0.3,
                     color_discrete_sequence=px.colors.sequential.YlOrRd_r)
        fig.update_layout(height=300, width=300,
                          showlegend=False, template='simple_white')
        return fig, {'display': 'none'}

# programme decision distribution


@app.callback(
    Output('programme_decision_distribution', 'figure'),
    Output('back-btn', 'style'),  # to hide/unhide the back button
    [Input('programme_decision_distribution', 'clickData'),  # for getting the vendor name from graph
     Input('back-btn', 'n_clicks'),
     Input('faculty_selection', 'value'),
     Input('programme_selection', 'value'),
     Input('attendance_type', 'value'),
     Input('academic_year', 'value'),
     Input('semester', 'value')
     ]
)
def programme_decision_drilldown(click_data, n_clicks, faculty, programme, attendancetype, academicyear, semester):
    df = data[(data['faculty'] == faculty) & (data['programme'] == programme) & (data['attendancetype']
                                                                                 == attendancetype) & (data['academicyear'] == academicyear) & (data['semester'] == semester)]

    # using callback context to check which input was fired
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == 'programme_decision_distribution':

        # get vendor name from clickData
        if click_data is not None:
            decision = click_data['points'][0]['label']

            if decision in df.decision.unique():
                # creating df for clicked vendor
                grouped_data = df[df['decision'] == decision].groupby(
                    by='module')['regnum'].nunique().sort_values(ascending=False).reset_index(name="Students")

                # generating product sales bar graph
                fig = px.bar(grouped_data, x='module',
                             y='Students', color='module')
                fig.update_layout(title=f'<b>Students distribution({decision})<b>',
                                  showlegend=False, template='simple_white', width=300, height=300)
                # returning the fig and unhiding the back button
                return fig, {'display': 'block'}

            else:
                data_grouped = df.groupby(by="decision")[
                    'regnum'].nunique().reset_index(name="Students")
                fig = px.pie(data_grouped, values='Students', names='decision',
                             hole=0.3,
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             title=f"<b>Decision Distribution {df.regnum.nunique()}</b>")
                fig.update_layout(height=300, width=300, showlegend=False,
                                  template='simple_white')
                return fig, {'display': 'none'}  # hiding the back button

    else:
        data_grouped = df.groupby(by="decision")[
            'regnum'].nunique().reset_index(name="Students")
        fig = px.pie(data_grouped, values='Students', names='decision',
                     hole=0.3,
                     color_discrete_sequence=px.colors.sequential.RdBu,
                     title=f"<b>Decision Distribution {df.regnum.nunique()}</b>")
        fig.update_layout(height=300, width=300, showlegend=False,
                          template='simple_white')
        return fig, {'display': 'none'}


if __name__ == "__main__":
    app.run_server(debug=True)
