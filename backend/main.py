from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/api/data/infections')
def hello_world():
    return jsonify({
        'dataSets': [{ 'data': [1, 2, 3, 4, 5], 'label': 'test' }],
        'labels': [ '11.03', '12.03', '13.03', '14.03', '15.03' ]
    })
