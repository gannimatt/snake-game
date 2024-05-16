from src import mongodb
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store_game_result', methods=['POST'])
def store_game_result_route():
    try:
        data = request.get_json()
        mongodb.store_game_result(data['username'], data['score'])
        return jsonify({'message': 'Game result stored successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dump_data_to_json', methods=['POST'])
def dump_data_to_json_route():
    output_file_path = "output.json"
    try:
        mongodb.dump_data_to_json(output_file_path)
        return jsonify({'message': 'Data dumped to JSON file successfully'})
    except IOError as e:
        return jsonify({'error': 'IO Error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)