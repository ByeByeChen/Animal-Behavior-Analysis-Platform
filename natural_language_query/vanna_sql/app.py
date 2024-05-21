from flask import Flask, request, jsonify
import getpass
import os
import MyVanna

os.environ["OPENAI_API_KEY"] = getpass.getpass()

app = Flask(__name__)

@app.route('/chat2db', methods=['POST'])
def query():
    vn = MyVanna(config={'api_key': 'sk-...', 'model': 'gpt-4-...'})
    vn.connect_to_mysql(host='192.168.1.169', dbname='platform_database', user='root', password='root', port=3306)

    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    plan = vn.get_training_plan_generic(df_information_schema)
    vn.train(plan=plan)
    data = request.get_json()
    query_text = data.get('query_text')
    response = vn.ask(question=query_text)

    return jsonify({'quesetion_result': response})

if __name__ == '__main__':
    app.run()