from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS, cross_origin
from defog import Defog
import decimal

class JsonEncoder(JSONEncoder):
    # for handling decimals
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)

defog = Defog()

app = Flask(__name__)
app.json_provider_class = JsonEncoder
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['POST'])
@cross_origin()
def test_defog():
    data = request.json
    question = data.get('question')
    previous_context = data.get('previous_context')
    results = defog.run_query(question=question, previous_context=previous_context)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)