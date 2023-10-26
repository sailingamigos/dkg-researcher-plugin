"""Main module"""

import json
import quart
import quart_cors
from maestro import get_answer, load_data, log_to_influxdb
from quart import request, jsonify
from influxdb import InfluxDBClient

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('mydb')

@app.post("/ask")
async def ask_question():
    """Ask a question"""
    data = await request.get_json()
    response = get_answer(data)

    is_empty = 1 if not response else 0
    log_to_influxdb(client, data, response, is_empty)

    return jsonify(response)

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

def main():
    """Main function"""
    load_data ('./assets_bot/cache/assets.jsonld')
    app.run(debug=True, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    main()
