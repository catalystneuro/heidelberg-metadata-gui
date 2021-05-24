import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
from jsonschema import validate
import json
import yaml
import base64
from json_schema_to_dash_forms.forms import SchemaFormContainer
from pathlib import Path
import flask
import importlib.resources as pkg_resources

from .. import examples


class MetadataForms(html.Div):
    def __init__(self, parent_app):
        """
        Forms to interface user input with metadata.

        INPUT:
        ------
        parent_app : running Dash app
        """
        super().__init__([])
        self.parent_app = parent_app
        self.export_controller = False
        self.convert_controller = False
        self.get_metadata_controller = False

        self.downloads_path = Path(__file__).parent.parent.absolute() / 'downloads'

        if not self.downloads_path.is_dir():
            self.downloads_path.mkdir()

        self.metadata_forms = SchemaFormContainer(
            id='metadata',
            schema=dict(),
            parent_app=self.parent_app
        )

        # If no schema file was passed, get metadata schema from basic examples
        schema_path = parent_app.server.config['JSON_SCHEMA_PATH']
        if Path(schema_path).is_file() and schema_path.split('.')[-1] == 'json':
            with open(schema_path) as f:
                self.metadata_json_schema = json.load(f)
        else:
            with pkg_resources.open_text(examples, 'schema_metadata_custom.json') as f:
                self.metadata_json_schema = json.load(f)

        self.metadata_forms.schema = self.metadata_json_schema
        self.metadata_forms.construct_children_forms()

        self.style = {'background-color': '#f0f0f0', 'min-height': '100vh'}

        self.children = [
            dbc.Container([
                html.Div(id='alerts-div'),
                dbc.Row([
                    html.Br(),
                    dbc.Col([
                        dbc.Label('Load a JSON schema: ', id='upload-file-label'),
                        dcc.Upload(
                            id='upload-json-schema',
                            children=[
                                'Drag and drop or Select Files',
                            ],
                            style={
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                            },

                        ),
                        dbc.Button('Schema to Forms', id='upload-json-button', color='dark', style={'margin-top': '10px'})
                    ], width=6)
                ], style={"justify-content": 'center', 'padding-top': '20px'}),
                dbc.Row([
                    dbc.Col(
                        dcc.Upload(dbc.Button('Load Metadata', color='dark'), id='button_load_metadata'),
                        width={'size': 2},
                        style={'justify-content': 'left', 'text-align': 'left', 'margin-top': '1%'},
                    ),
                    dbc.Col(
                        html.Div([
                            dbc.Button('Export Metadata', id='button_export_metadata', color='dark'),#, style={'display': 'none'}),
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
                        dbc.Button('Refresh', id='button_refresh', color='dark'),
                        width={'size': 2},
                        style={'justify-content': 'left', 'text-align': 'left', 'margin-top': '1%'},
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        dbc.Alert(
                            children=[],
                            id="alert_required_source",
                            dismissable=True,
                            is_open=False,
                            color='danger'
                        )
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
                dbc.Row([
                    dbc.Col(
                        dbc.Alert(
                            children=[],
                            id="alert_validation",
                            dismissable=True,
                            is_open=False,
                            color='danger'
                        )
                    )
                ]),
                dbc.Row(
                    dbc.Col(
                        id='metadata-col',
                        children=self.metadata_forms,
                        width={'size': 12}
                    ),
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
                Output('alerts-div', 'children'),
                Output('upload-file-label', 'children')
            ],
            [
                Input('upload-json-schema', 'contents')
            ],
            [
                State('upload-json-schema', 'filename')
            ]
        )
        def get_metadata_schema(contents, filename):
            ctx = dash.callback_context
            if not ctx.triggered:
                return [dash.no_update, dash.no_update]

            if not filename.endswith('.json'):
                alert = dbc.Row([dbc.Col(dbc.Alert('File must be a json.', color='danger', dismissable=True, is_open=True), width={'size': 4})], style={'justify-content': 'center'})
                return [alert, dash.no_update]

            label_message = f'Schema file:   {filename}'

            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            json_schema = json.loads(decoded)

            self.metadata_json_schema = json_schema
            self.get_metadata_controller = True

            return [dash.no_update, label_message]

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
                Output('get_metadata_done', 'n_clicks'),
                Output('alert_required_source', 'is_open'),
                Output('alert_required_source', 'children')
            ],
            [Input('upload-json-button', 'n_clicks')],
            [
                State('alert_required_source', 'is_open'),
                State('button_load_metadata', 'style'),
                State('button_export_metadata', 'style'),
                State('button_refresh', 'style'),
            ]
        )
        def get_metadata(trigger, alert_is_open, *styles):
            """
            Render Metadata forms based on Source Data Form
            This function is triggered when sourcedata internal dict is updated
            and get metadata controller is setted to true.
            If get metadata controller is not setted to true but the sourcedata
            internal dict was updated the function will return the current
            application state
            """

            if not trigger or not self.get_metadata_controller:
                return [dash.no_update, {'display': 'block'}, {'display': 'block'}, {'display': 'block'},
                        None, alert_is_open, []]

            self.get_metadata_controller = False

            # Clean form children if exists to render new one
            if self.metadata_forms.children_forms:
                self.metadata_forms.children_forms = []
                self.metadata_forms.data = {}

            self.metadata_forms.schema = self.metadata_json_schema
            self.metadata_forms.construct_children_forms()

            return [self.metadata_forms, {'display': 'block'}, {'display': 'block'},
                    {'display': 'block'}, 1, alert_is_open, []]

        @self.parent_app.callback(
            Output({'type': 'external-trigger-update-links-values', 'index': 'metadata-external-trigger-update-links-values'}, 'children'),
            [Input('button_refresh', 'n_clicks')]
        )
        def refresh_forms_links(click):
            if click:
                return str(np.random.rand())

        @self.parent_app.callback(
            [
                Output({'type': 'external-trigger-update-forms-values', 'index': 'metadata-external-trigger-update-forms-values'}, 'children'),
                Output('alert_validation', 'is_open'),
                Output('alert_validation', 'children')
            ],
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
                return [], False, dash.no_update

            if trigger_source != 'button_load_metadata' and click is not None:
                # Trigger update of React components
                output = str(np.random.rand())
                return output, False, dash.no_update

            _, content_string = contents.split(',')
            filename_extension = filename.split('.')[-1]

            # Update SchemaFormContainer internal data dictionary
            if filename_extension == 'json':
                bs4decode = base64.b64decode(content_string)
                json_string = bs4decode.decode('utf8').replace("'", '"')
                new_metadata = json.loads(json_string)
            elif filename_extension in ['yaml', 'yml']:
                bs4decode = base64.b64decode(content_string)
                yaml_data = yaml.load(bs4decode, Loader=yaml.BaseLoader)
                new_metadata = yaml_data

            # Validate agains current schema
            try:
                validate(instance=new_metadata, schema=self.metadata_json_schema)
            except Exception as er:
                validation_error = f'\nFailed because: {er.message}'
                return dash.no_update, True, validation_error

            # If validated, update forms
            self.metadata_json_data = new_metadata
            self.metadata_forms.update_data(data=self.metadata_json_data)

            # Trigger update of React components
            output = str(np.random.rand())
            return output, False, dash.no_update

        @self.parent_app.server.route('/downloads/<path:filename>')
        def download_file(filename):
            return flask.send_from_directory(
                self.downloads_path,
                filename,
                as_attachment=True
            )
