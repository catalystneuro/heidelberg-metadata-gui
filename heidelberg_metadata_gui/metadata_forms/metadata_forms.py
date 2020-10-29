import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import json
import yaml
import base64
from json_schema_to_dash_forms.forms import SchemaFormContainer
from pathlib import Path
import flask


class MetadataForms(html.Div):
    def __init__(self, parent_app, converter_class):
        """
        Forms to interface user input with metadata.

        INPUT:
        ------
        parent_app : running Dash app
        converter : NWB converter class
        """
        super().__init__([])
        self.parent_app = parent_app
        self.converter_class = converter_class
        self.export_controller = False
        self.convert_controller = False
        self.get_metadata_controller = False

        self.downloads_path = Path(__file__).parent.parent.absolute() / 'downloads'

        self.source_json_schema = converter_class.get_input_schema()

        # Source data Form
        self.source_forms = SchemaFormContainer(
            id='sourcedata',
            schema=self.source_json_schema,
            parent_app=self.parent_app
        )

        self.metadata_forms = SchemaFormContainer(
            id='metadata',
            schema=dict(),
            parent_app=self.parent_app
        )
        self.style = {'background-color': '#f0f0f0', 'min-height': '100vh'}

        self.children = [
            dbc.Container([
                dbc.Row([
                    html.Br(),
                    dbc.Col(self.source_forms, width={'size': 12}),
                    dbc.Col(
                        dbc.Button('Get Metadata Form', id='get_metadata_btn'),
                        style={'justify-content': 'left', 'text-align': 'left', 'margin-top': '1%'},
                        width={'size': 4}
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        dcc.Upload(dbc.Button('Load Metadata', color='dark'), id='button_load_metadata', style={'display': 'none'}),
                        width={'size': 2},
                        style={'justify-content': 'left', 'text-align': 'left', 'margin-top': '1%'},
                    ),
                    dbc.Col(
                        html.Div([
                            dbc.Button('Export Metadata', id='button_export_metadata', color='dark', style={'display': 'none'}),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody([
                                        html.Div([
                                            html.A(
                                                dbc.Button("Download as JSON", id='button_export_json', color="link"),
                                                href='/downloads/exported_metadata.json'
                                            ),
                                            html.A(
                                                dbc.Button("Download as YAML", id='button_export_yaml', color="link"),
                                                href='/downloads/exported_metadata.yaml'
                                            )
                                        ])
                                    ])
                                ],
                                id="popover_export_metadata",
                                target='button_export_metadata',
                                is_open=False,
                                placement='top',
                            )
                        ]),
                        width={'size': 2},
                        style={'justify-content': 'left', 'text-align': 'left', 'margin-top': '1%'},
                    ),
                    dbc.Col(
                        dbc.Button('Refresh', id='button_refresh', color='dark', style={'display': 'none'}),
                        width={'size': 2},
                        style={'justify-content': 'left', 'text-align': 'left', 'margin-top': '1%'},
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        dbc.Alert(
                            children=[],
                            id="alert_required",
                            dismissable=True,
                            is_open=False,
                            color='danger'
                        )
                    )
                ]),
                dbc.Row(
                    dbc.Col(id='metadata-col', width={'size': 12}),
                    style={'margin-top': '1%', 'margin-bottom': '10px'}
                ),
                html.Br(),
                html.Div(id='export-output', style={'display': 'none'}),
                html.Div(id='export-input', style={'display': 'none'}),
                dbc.Button(id='get_metadata_done', style={'display': 'none'})
            ], style={'min-height': '110vh'})
        ]

        @self.parent_app.callback(
            [
                Output("popover_export_metadata", "is_open"),
                Output('alert_required', 'is_open'),
                Output('alert_required', 'children'),
            ],
            [Input('metadata-output-update-finished-verification', 'children')],
            [
                State("popover_export_metadata", "is_open"),
                State('alert_required', 'is_open')
            ]
        )
        def export_metadata(trigger, fileoption_is_open, req_is_open):
            """
            Export Metadata Form data to JSON and YAML file
            This function is triggered when metadata internal dict is updated
            and export controller is setted to true.
            If export controller is not setted to true but the metadata internal dict was updated
            the function will return the current application state
            """


            # Prevent default
            if not self.export_controller or not trigger:
                return fileoption_is_open, req_is_open, []

            if self.export_controller and fileoption_is_open:
                self.export_controller = False
                return not fileoption_is_open, req_is_open, []

            alerts, output = self.metadata_forms.data_to_nested()

            # If required fields missing return alert
            if alerts is not None:
                return fileoption_is_open, not req_is_open, alerts

            # Make temporary files on server side
            # JSON
            exported_file_path = self.downloads_path / 'exported_metadata.json'
            with open(exported_file_path, 'w') as outfile:
                json.dump(output, outfile, indent=4)

            # YAML
            exported_file_path = self.downloads_path / 'exported_metadata.yaml'
            with open(exported_file_path, 'w') as outfile:
                yaml.dump(output, outfile, default_flow_style=False)

            return not fileoption_is_open, req_is_open, []

        @self.parent_app.callback(
            Output('metadata-external-trigger-update-internal-dict', 'children'),
            [
                Input('button_export_metadata', 'n_clicks')
            ],
        )
        def update_internal_metadata(click_export):
            """
            Trigger metadata internal dict update and then:
            1) set export_controller to true, when exporting to json/yaml
            2) set convert_controller to true, when running conversion
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                return dash.no_update
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                if button_id == 'button_export_metadata':
                    self.export_controller = True
                    self.convert_controller = False
                return str(np.random.rand())

        @self.parent_app.callback(
            [
                Output('metadata-col', 'children'),
                Output('button_load_metadata', 'style'),
                Output('button_export_metadata', 'style'),
                Output('button_refresh', 'style'),
                Output('get_metadata_done', 'n_clicks')
            ],
            [Input('sourcedata-output-update-finished-verification', 'children')],
            [
                State('button_load_metadata', 'style'),
                State('button_export_metadata', 'style'),
                State('button_refresh', 'style')
            ]
        )
        def get_metadata(trigger, *styles):
            """
            Render Metadata forms based on Source Data Form
            This function is triggered when sourcedata internal dict is updated
            and get metadata controller is setted to true.
            If get metadata controller is not setted to true but the sourcedata
            internal dict was updated the function will return the current
            application state
            """

            if not trigger or not self.get_metadata_controller:
                # If metadata forms defined reset to default state
                if self.metadata_forms.children_forms:
                    self.metadata_forms.children_forms = []
                    self.metadata_forms.children = self.metadata_forms.children_triggers
                    self.metadata_forms.data = dict()
                    self.metadata_forms.schema = dict()
                return [self.metadata_forms, styles[0], styles[1], styles[2], None]

            # Get forms data
            alerts, source_data = self.source_forms.data_to_nested()

            self.get_metadata_controller = False

            # Get metadata schema from converter
            self.converter = self.converter_class(input_data=source_data)
            self.metadata_json_schema = self.converter.get_metadata_schema()

            # Get metadata data from converter
            self.metadata_json_data = self.converter.get_metadata()

            if self.metadata_forms.children_forms:
                # Clean form children if exists to render new one
                self.metadata_forms.children_forms = []

            self.metadata_forms.schema = self.metadata_json_schema
            self.metadata_forms.construct_children_forms()
            self.metadata_forms.update_data(data=self.metadata_json_data)

            return [self.metadata_forms, {'display': 'block'}, {'display': 'block'},
                    {'display': 'block'}, 1]

        @self.parent_app.callback(
            Output('sourcedata-external-trigger-update-internal-dict', 'children'),
            [Input('get_metadata_btn', 'n_clicks')]
        )
        def update_internal_sourcedata(click):
            """Update sourcedata internal dictionary to Get Metadata Forms from it"""
            if click:
                self.get_metadata_controller = True
                return str(np.random.rand())

        @self.parent_app.callback(
            Output({'type': 'external-trigger-update-links-values', 'index': 'metadata-external-trigger-update-links-values'}, 'children'),
            [Input('button_refresh', 'n_clicks')]
        )
        def refresh_forms_links(click):
            if click:
                return str(np.random.rand())

        @self.parent_app.callback(
            Output({'type': 'external-trigger-update-forms-values', 'index': 'metadata-external-trigger-update-forms-values'}, 'children'),
            [
                Input('button_load_metadata', 'contents'),
                Input('get_metadata_done', 'n_clicks')
            ],
            [State('button_load_metadata', 'filename')]
        )
        def update_forms_values_metadata(contents, click, filename):
            """
            Updates forms values (except links) when:
            - Forms are created (receives metadata dict from Converter)
            - User uploads metadata json / yaml file
            """
            ctx = dash.callback_context
            trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]

            if trigger_source != 'button_load_metadata' and click is None:
                output = []
                return output

            if trigger_source != 'button_load_metadata' and click is not None:
                output = str(np.random.rand())
                return output

            content_type, content_string = contents.split(',')
            filename_extension = filename.split('.')[-1]

            # Update SchemaFormContainer internal data dictionary
            if filename_extension == 'json':
                bs4decode = base64.b64decode(content_string)
                json_string = bs4decode.decode('utf8').replace("'", '"')
                self.metadata_json_data = json.loads(json_string)
                self.metadata_forms.update_data(data=self.metadata_json_data)
            elif filename_extension in ['yaml', 'yml']:
                bs4decode = base64.b64decode(content_string)
                yaml_data = yaml.load(bs4decode, Loader=yaml.BaseLoader)
                self.metadata_json_data = yaml_data
                self.metadata_forms.update_data(data=self.metadata_json_data)
            # Trigger update of React components
            output = str(np.random.rand())

            return output

        @self.parent_app.server.route('/downloads/<path:filename>')
        def download_file(filename):
            return flask.send_from_directory(
                directory=self.downloads_path,
                filename=filename,
                as_attachment=True
            )
