from flask import Flask, request, Response
import json
# 导入 AI 算法
import ai_list

app = Flask(__name__)

# 跨域支持
@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Method'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


# AI 的 API 支持
ai_map = [{
    'name': '随机',
    'description': '随机下棋.',
}]
ai_map_api = [ai_list.random_ai, ai_list.jie_giegie, ai_list.czz, ai_list.away]

@app.route('/ai_list', methods=['GET'])
def get_ai_map():
    return Response(json.dumps(ai_map), mimetype='application/json')

@app.route('/ai_api', methods=['POST'])
def ai_api():
    data: dict = request.json
    aiIndex, board, current, newest, reversal, prompt = data.values()
    return Response(json.dumps(ai_map_api[aiIndex](board, current, newest, reversal, prompt)), mimetype='application/json')


# 挂载
if __name__ == '__main__':
    app.run(debug=False, port=7685)
