from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/1/boudary', methods=['GET'])
def get_data():
    # 读取CSV文件
    df = pd.read_csv('triangle-boundary.csv')

    # 转换为JSON格式
    data_json = df.to_json(orient='records', force_ascii=False)
    data = {"message": "Hello from Flask!"}
    return jsonify(data_json)

@app.route('/2/equal', methods=['GET'])
def get_data_2_equal():
    # 读取CSV文件
    df = pd.read_csv('triangle-boundary.csv')

    # 转换为JSON格式
    data_json = df.to_json(orient='records', force_ascii=False)
    data = {"message": "Hello from Flask!"}
    return jsonify(data_json)

@app.route('/api/data', methods=['POST'])
def post_data():
    received_data = request.json
    response_data = {"received": received_data}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
