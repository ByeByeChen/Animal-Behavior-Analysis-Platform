from flask import Flask, request, jsonify
import getpass
import os
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent

os.environ["OPENAI_API_KEY"] = getpass.getpass()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def query():
    db = SQLDatabase.from_uri("mysql://root:root@192.168.1.169/platform_database")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = create_sql_query_chain(llm, db)

    data = request.get_json()
    query_text = data.get('query_text')
    response = chain.invoke({"question": query_text})
    
    return jsonify({'sql_result': response})

@app.route('/excute_sql', methods=['POST'])
def excute_sql():
    db = SQLDatabase.from_uri("mysql://root:root@192.168.1.169/platform_database")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
    chain = write_query | execute_query

    data = request.get_json()
    query_text = data.get('query_text')
    response = chain.invoke({"question": query_text})
    
    return jsonify({'quesetion_result': response})

@app.route('/answer_question', methods=['POST'])
def answer_question():
    db = SQLDatabase.from_uri("mysql://root:root@192.168.1.169/platform_database")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
 
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )

    answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
    )
    data = request.get_json()
    query_text = data.get('query_text')
    response = chain.invoke({"question": query_text})
    return jsonify({'quesetion_result': response})

@app.route('/chat2db', methods=['POST'])
def chat2db():
    db = SQLDatabase.from_uri("mysql://root:root@192.168.1.169/platform_database")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    data = request.get_json()
    query_text = data.get('query_text')
    response = agent_executor.invoke({"input": query_text})
    
    return jsonify({'quesetion_result': response})

if __name__ == '__main__':
    app.run()