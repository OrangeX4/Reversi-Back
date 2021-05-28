from flask import Flask, request, Response
import json
# from flask_cors import CORS
# 导入 AI 算法
import ai_list

app = Flask(__name__)
# CORS(app, supports_credentials=True)

# 跨域支持
@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Method'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

ai_map = [{
    'name': '⑨',
    'description': '脑袋有些笨笨的.',
}]
ai_map_api = [ai_list.random_ai]

@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/ai_list', methods=['GET'])
def get_ai_map():
    return Response(json.dumps(ai_map), mimetype='application/json')

@app.route('/ai_api', methods=['POST'])
def ai_api():
    data: dict = request.json
    aiIndex, board, current, newest, reversal, prompt = data.values()
    return Response(json.dumps(ai_map_api[aiIndex](board, current, newest, reversal, prompt)), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
