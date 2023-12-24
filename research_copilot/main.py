"""Main module"""

import quart
import quart_cors
from maestro import get_answer, load_knowledge_assets, connect_to_otnode, perform_kmeans, perform_regression, log_to_influxdb
from quart import request, jsonify, redirect
from influxdb import InfluxDBClient

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

client = InfluxDBClient(host='localhost', port=3000)
client.switch_database('mydb')

@app.get("/")
async def index():
    """Demo page"""
    return redirect("https://github.com/sailingamigos/dkg-researcher-plugin/tree/main/docs/demo.md")

@app.get("/data")
async def get_assets():
    """Return list of assets"""
    return redirect ("https://github.com/sailingamigos/dkg-researcher-plugin/tree/main/knowledge_assets")

@app.get("/privacy")
async def privacy():
    """Privacy page"""
    return redirect("https://www.gnu.org/licenses/gpl-3.0.en.html")

@app.get("/logo.jpg")
async def plugin_logo():
    """Return plugin logo"""
    filename = './.well-known/logo.jpg'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """Return plugin manifest"""
    with open("./.well-known/ai-plugin.json", encoding="utf-8") as file:
        text = file.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    """Return plugin API specification"""
    with open("./.well-known/openapi.yaml", encoding="utf-8") as file:
        text = file.read()
        return quart.Response(text, mimetype="text/yaml")

@app.post("/ask")
async def ask_question():
    """Ask a question"""
    response = []

    payload = await request.get_json()
    sparql_query = payload['scholarlyArticleSparqlQuery']
    result = get_answer(sparql_query)
    is_empty = 1 if not response else 0
    log_to_influxdb(client, sparql_query, result, is_empty)
    response += result

    sparql_query = payload['arxivSparqlQuery']
    result = get_answer(sparql_query)
    is_empty = 1 if not response else 0
    log_to_influxdb(client, sparql_query, result, is_empty)
    response += result

    return jsonify(response)

@app.post("/kmeans")
async def kmeans_api():
    """Endpoint for KMeans clustering"""
    data = await request.get_json()
    result = perform_kmeans(data)
    return jsonify(result)

@app.post("/linear_regression")
async def linear_regression_api():
    """Endpoint for linear regression"""
    data = await request.get_json()
    result = perform_regression(data)
    return jsonify(result)

def main():
    """Main function"""
    connect_to_otnode()
    load_knowledge_assets('knowledge_assets')
    app.run(debug=True, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
