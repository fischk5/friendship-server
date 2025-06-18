from flask import Flask, request, jsonify
from utils import ExpensesProcesser
import threading

app = Flask(__name__)

processor = ExpensesProcesser()

@app.route("/transactions", methods=["POST"])
def handle_transaction():
    if "file" not in request.files:
        return jsonify({"error": "File is missing"}), 400
    
    file = request.files['file']
    processor.write_csv_file_to_server(file, "data.csv")

    thread = threading.Thread(target=processor.process_report_async, args=())
    thread.start()

    return jsonify({ "success": True, "message": "File saved. Processing started." })
    

@app.route("/report", methods=["GET"])
def get_report():
    report = processor.get_report_from_server()
    return jsonify(report ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


