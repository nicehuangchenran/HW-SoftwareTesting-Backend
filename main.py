import ast
import os
import flask
import pandas as pd
import time
import datetime
from flask import Flask, request
from flask_cors import CORS
from hw_telephone import telephone
from decimal import Decimal
from http import HTTPStatus
from decimal import Decimal, getcontext, InvalidOperation

app = Flask(__name__)

cors_config = {
    r"/api/*": {"origins": "*"}
}
CORS(app, resources=cors_config)

def replace_empty_with_dash(df):
    df = df.fillna('-')
    return df

@app.route('/api/TelecomCharge_data', methods=['GET'])
def telecom_charge_data():
    value = request.args.get('value')
    file_mapping = {
        '1': 'test_case/telephone_boundary.csv',
        '2': 'test_case/telephone_equivalent.csv',
        '3': 'test_case/telephone_decision.csv'
    }

    file_path = file_mapping.get(value)
    if not file_path:
        return flask.jsonify({"message": "Invalid value parameter"}), HTTPStatus.BAD_REQUEST

    try:
        df = pd.read_csv(file_path)
        df = replace_empty_with_dash(df)
    except FileNotFoundError:
        return flask.jsonify({"message": "Test case file not found"}), HTTPStatus.NOT_FOUND

    return flask.jsonify({"tableData": ast.literal_eval(df.to_json(orient='records'))})

@app.route('/api/TelecomCharge_result', methods=['GET'])
def telecom_charge_result():
    value = request.args.get('value')
    file_mapping = {
        '1': 'test_case/telephone_boundary.csv',
        '2': 'test_case/telephone_equivalent.csv',
        '3': 'test_case/telephone_decision.csv'
    }

    file_path = file_mapping.get(value)
    if not file_path:
        return flask.jsonify({"message": "Invalid value parameter"}), HTTPStatus.BAD_REQUEST

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return flask.jsonify({"message": "Test case file not found"}), HTTPStatus.NOT_FOUND

    total_count = df.shape[0]
    pass_count = 0
    fail_count = 0

    for i in range(total_count):
        df.iloc[i, 4] = telephone.telephone(df.iloc[i, 1], df.iloc[i, 2])
        df.iloc[i, 7] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.iloc[i, 8] = "2151300"
        df.iloc[i, 9] = ""

        try:
            expected_output = float(df.iloc[i, 3])
            actual_output = float(df.iloc[i, 4])
        except ValueError:
            expected_output = str(df.iloc[i, 3])
            actual_output = str(df.iloc[i, 4])
        
        if expected_output != actual_output:
            df.iloc[i, 5] = "N"
            fail_count += 1
        else:
            df.iloc[i, 5] = "Y"
            pass_count += 1

    df = replace_empty_with_dash(df)
    result_directory = "test result"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    df.to_csv(os.path.join(result_directory, f"telephone_result_{value}.csv"), index=False)

    chart_data = [
        {"name": "Y", "value": pass_count},
        {"name": "N", "value": fail_count}
    ]

    return flask.jsonify({
        "tableData": ast.literal_eval(df.to_json(orient='records')),
        "chartData": chart_data
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
