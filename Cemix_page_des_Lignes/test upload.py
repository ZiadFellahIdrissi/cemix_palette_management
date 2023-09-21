import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Password Protected App"),
    html.Label("Enter Password:"),
    dcc.Input(id="password-input", type="password"),
    html.Div(id="password-verification"),
    dcc.Input(id="input-1", type="text", disabled=True),
    dcc.Input(id="input-2", type="text", disabled=True),
    dcc.Input(id="input-3", type="text", disabled=True),
    dcc.Input(id="input-4", type="text", disabled=True),
    html.Button("Button 1", id="button-1", disabled=True),
    html.Button("Button 2", id="button-2", disabled=True),
    html.Button("Button 3", id="button-3", disabled=True),
    html.Button("Button 4", id="button-4", disabled=True)
])

@app.callback(
    Output("password-verification", "children"),
    Output("input-1", "disabled"),
    Output("input-2", "disabled"),
    Output("input-3", "disabled"),
    Output("input-4", "disabled"),
    Output("button-1", "disabled"),
    Output("button-2", "disabled"),
    Output("button-3", "disabled"),
    Output("button-4", "disabled"),
    Input("password-input", "value")
)
def verify_password(password):
    # Replace 'your_password' with the actual correct password
    correct_password = 'your_password'
    
    if password == correct_password:
        return "Password is correct.", False, False, False, False, False, False, False, False
    else:
        return "Password is incorrect.", True, True, True, True, True, True, True, True

if __name__ == '__main__':
    app.run_server(debug=True)
