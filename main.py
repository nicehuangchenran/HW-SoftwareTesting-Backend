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
from flask import Flask, jsonify  

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

        if str(Decimal(str(df.iloc[i, 3])).normalize()) != df.iloc[i, 4]:
            df.iloc[i, 5] = "N"
            fail_count += 1
        else:
            df.iloc[i, 5] = "Y"
            pass_count += 1

    df = replace_empty_with_dash(df)
    result_directory = "test result"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    df.to_csv(os.path.join(result_directory,
              f"telephone_result_{value}.csv"), index=False)

    chart_data = [
        {"name": "Y", "value": pass_count},
        {"name": "N", "value": fail_count}
    ]

    return flask.jsonify({
        "tableData": ast.literal_eval(df.to_json(orient='records')),
        "chartData": chart_data
    })



# --------------------------------hcr---------------------------------

# @app.route('/api/Triangle_data', methods=['GET'])
# def telecom_charge_data2():
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     value = request.args.get('value')
#     file_mapping = {
#         '1': os.path.join(current_directory,'test_case','q1','triangle_boundary.csv'),
#         '2': os.path.join(current_directory,'test_case','q1','triangle_equivalent.csv'),
#     }

#     file_path = file_mapping.get(value)
#     if not file_path:
#         return flask.jsonify({"message": "Invalid value parameter"}), HTTPStatus.BAD_REQUEST

#     try:
#         df = pd.read_csv(file_path)
#         df = replace_empty_with_dash(df)
#     except FileNotFoundError:
#         return flask.jsonify({"message": "Test case file not found"}), HTTPStatus.NOT_FOUND

#     return flask.jsonify({"tableData": df.to_json(orient='records')})
#     # return flask.jsonify({"tableData": ast.literal_eval(df.to_json(orient='records'))})

# @app.route('/api/Triangle_result', methods=['GET'])
# def telecom_charge_result2():
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     value = request.args.get('value')
#     file_mapping = {
#         '1': os.path.join(current_directory,'test result', 'q1', 'triangle_boundary.csv'),
#         '2': os.path.join(current_directory,'test result', 'q1', 'triangle_equivalent.csv'),
#     }

#     file_path = file_mapping.get(value)
#     if not file_path:
#         return flask.jsonify({"message": "Invalid value parameter"}), HTTPStatus.BAD_REQUEST

#     try:
#         df = pd.read_csv(file_path)
#     except FileNotFoundError:
#         return flask.jsonify({"message": "Test case file not found"}), HTTPStatus.NOT_FOUND

#     total_count = df.shape[0]
#     pass_count = 0
#     fail_count = 0

#     for i in range(total_count):
#         df.iloc[i, 4] = telephone.telephone(df.iloc[i, 1], df.iloc[i, 2])
#         df.iloc[i, 7] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         df.iloc[i, 8] = "2151300"
#         df.iloc[i, 9] = ""

#         if str(Decimal(str(df.iloc[i, 3])).normalize()) != df.iloc[i, 4]:
#             df.iloc[i, 5] = "N"
#             fail_count += 1
#         else:
#             df.iloc[i, 5] = "Y"
#             pass_count += 1

#     df = replace_empty_with_dash(df)
#     result_directory = "test result"
#     if not os.path.exists(result_directory):
#         os.makedirs(result_directory)

#     df.to_csv(os.path.join(result_directory,
#               f"telephone_result_{value}.csv"), index=False)

#     chart_data = [
#         {"name": "Y", "value": pass_count},
#         {"name": "N", "value": fail_count}
#     ]

#     return flask.jsonify({
#         "tableData": ast.literal_eval(df.to_json(orient='records')),
#         "chartData": chart_data
#     })


# --------------------------------P1---------------------------------

@app.route('/api/Triangle_data', methods=['GET'])
def get_triangle_boundary():  
    current_directory = os.path.dirname(os.path.abspath(__file__))
    value = request.args.get('value')
    file_mapping = {
        '1': os.path.join(current_directory,'test_case', 'q1', 'triangle_boundary.csv'),
        '2': os.path.join(current_directory,'test_case', 'q1', 'triangle_equivalent.csv'),
    }

    csv_path = file_mapping.get(value)
    print(csv_path)


    try:  
        df = pd.read_csv(csv_path)  
    except FileNotFoundError:  
        return jsonify({'error': f'File {csv_path} not found.'}), 404  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  
  
    # 将 DataFrame 转换为 JSON  
    # 如果你想要一个包含列表的 JSON，其中每个列表项是一个字典（代表 DataFrame 的一行）  
    # 你可以使用 to_dict 方法，并指定 'records' 作为参数  
    json_data = df.to_dict(orient='records')  
    print(df)
  
    return jsonify({'tableData':json_data})  

@app.route('/api/Triangle_result', methods=['GET'])
def get_triangle_result():  
    current_directory = os.path.dirname(os.path.abspath(__file__))
    value = request.args.get('value')
    file_mapping = {
        '1': os.path.join(current_directory,'test result','q1','triangle_boundary.csv'),
        '2': os.path.join(current_directory,'test result','q1','triangle_equivalent.csv'),
    }

    csv_path = file_mapping.get(value)
    

    try:  
        df = pd.read_csv(csv_path)  
    except FileNotFoundError:  
        return jsonify({'error': f'File {csv_path} not found.'}), 404  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  
   
    json_data = df.to_dict(orient='records')  
  
    pass_count=len(json_data)
    fail_count=0
    
    chart_data = [
        {"name": "Y", "value": pass_count},
        {"name": "N", "value": fail_count}
    ]
  
    return jsonify({'tableData':json_data,'chartData':chart_data}) 


# --------------------------------P2---------------------------------


@app.route('/api/Calendar_data', methods=['GET'])
def get_Calendar_data():  
    current_directory = os.path.dirname(os.path.abspath(__file__))
    value = request.args.get('value')
    file_mapping = {
        '1': os.path.join(current_directory,'test_case', 'q2', 'calendar_boundary.csv'),
        '2': os.path.join(current_directory,'test_case', 'q2', 'calendar_equivalent.csv'),
        '3': os.path.join(current_directory,'test_case', 'q2', 'calendar_decision.csv'),
    }

    csv_path = file_mapping.get(value)
    
    try:  
        df = pd.read_csv(csv_path)  
    except FileNotFoundError:  
        return jsonify({'error': f'File {csv_path} not found.'}), 404  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  
   
    json_data = df.to_dict(orient='records')  
  
    return jsonify({'tableData':json_data})  

@app.route('/api/Calendar_result', methods=['GET'])
def get_Calendar_result():  
    current_directory = os.path.dirname(os.path.abspath(__file__))
    value = request.args.get('value')
    file_mapping = {
        '1': os.path.join(current_directory,'test result', 'q2', 'calendar_boundary.csv'),
        '2': os.path.join(current_directory,'test result', 'q2', 'calendar_equivalent.csv'),
        '3': os.path.join(current_directory,'test result', 'q2', 'calendar_decision.csv'),
    }

    csv_path = file_mapping.get(value)
    

    try:  
        df = pd.read_csv(csv_path)  
    except FileNotFoundError:  
        return jsonify({'error': f'File {csv_path} not found.'}), 404  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  
   
    json_data = df.to_dict(orient='records')  
  
    pass_count=len(json_data)
    fail_count=0
    
    chart_data = [
        {"name": "Y", "value": pass_count},
        {"name": "N", "value": fail_count}
    ]
  
    return jsonify({'tableData':json_data,'chartData':chart_data}) 


# --------------------------------P3---------------------------------

@app.route('/api/ComputerSalesSystem_data', methods=['GET'])
def get_c_data():  
    current_directory = os.path.dirname(os.path.abspath(__file__))
    value = request.args.get('value')
    file_mapping = {
        '1': os.path.join(current_directory,'test_case', 'q3', 'computer_boundary.csv'),
    }

    csv_path = file_mapping.get(value)
    

    try:  
        df = pd.read_csv(csv_path)  
    except FileNotFoundError:  
        return jsonify({'error': f'File {csv_path} not found.'}), 404  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  
   
    json_data = df.to_dict(orient='records')  
  
    return jsonify({'tableData':json_data})  

@app.route('/api/ComputerSalesSystem_result', methods=['GET'])
def get_c_result():  
    current_directory = os.path.dirname(os.path.abspath(__file__))
    value = request.args.get('value')
    file_mapping = {
        '1': os.path.join(current_directory,'test result', 'q3', 'computer_boundary.csv'),
    }

    csv_path = file_mapping.get(value)
    

    try:  
        df = pd.read_csv(csv_path)  
    except FileNotFoundError:  
        return jsonify({'error': f'File {csv_path} not found.'}), 404  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  
   
    json_data = df.to_dict(orient='records')  
  
    pass_count=len(json_data)
    fail_count=0
    
    chart_data = [
        {"name": "Y", "value": pass_count},
        {"name": "N", "value": fail_count}
    ]
  
    return jsonify({'tableData':json_data,'chartData':chart_data})  


if __name__ == '__main__':
    app.run(debug=True, port=5000)
