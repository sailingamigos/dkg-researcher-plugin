"""Main module."""

import quart # pylint: disable=import-error
import quart_cors # pylint: disable=import-error
from maestro import (
    get_answer,
    load_knowledge_assets,
    connect_to_otnode,
    perform_kmeans,
    perform_regression,
    perform_vector_search,
    log_to_influxdb,
)
from quart import request, jsonify, redirect # pylint: disable=import-error
from influxdb import InfluxDBClient # pylint: disable=import-error

# Create a Quart app with CORS support
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Initialize InfluxDB client
client = InfluxDBClient(host='localhost', port=3000)
client.switch_database('mydb')

@app.get("/")
async def index():
    """Redirect to the demo page."""
    return redirect("https://github.com/sailingamigos/dkg-researcher-plugin/tree/main/docs/demo.md")

@app.get("/data")
async def get_assets():
    """Redirect to the list of knowledge assets."""
    return redirect("https://github.com/sailingamigos/dkg-researcher-plugin/tree/main/knowledge_assets")

@app.get("/privacy")
async def privacy():
    """Redirect to the privacy page."""
    return redirect("https://www.gnu.org/licenses/gpl-3.0.en.html")

@app.get("/logo.jpg")
async def plugin_logo():
    """Return the plugin logo image."""
    filename = './.well-known/logo.jpg'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    """Return the plugin manifest."""
    with open("./.well-known/ai-plugin.json", encoding="utf-8") as file:
        text = file.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    """Return the plugin API specification."""
    with open("./.well-known/openapi.yaml", encoding="utf-8") as file:
        text = file.read()
        return quart.Response(text, mimetype="text/yaml")

@app.post("/ask")
async def ask_question_api():
    """Endpoint to ask a question."""
    payload = await request.get_json()
    result = get_answer(payload)
    is_empty = 1 if not result else 0
    log_to_influxdb(client, payload, result, is_empty)
    return jsonify(result)

@app.post("/kmeans")
async def kmeans_api():
    """Endpoint for KMeans clustering."""
    data = await request.get_json()
    result = perform_kmeans(data)
    return jsonify(result)

@app.post("/linear_regression")
async def linear_regression_api():
    """Endpoint for linear regression."""
    data = await request.get_json()
    result = perform_regression(data)
    return jsonify(result)

@app.post("/vector_search")
async def vector_search_api():
    """Endpoint for vector search."""
    data = await request.get_json()
    result = perform_vector_search(data)
    return jsonify(result)

def main():
    """Main function to start the app."""
    # connect_to_otnode()
    load_knowledge_assets('knowledge_assets')
    app.run(debug=True, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
