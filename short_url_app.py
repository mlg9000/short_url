#/usr/bin/python

from flask import Flask, request, jsonify

app = Flask(__name__)

encoded_urls = []
small_url_base = "http://smallurl/"

@app.route('/encode', methods=['POST'])
def encode_url ():
    """Encode Endpoint"""
    post_data     = request.get_json()
    long_url      = post_data["long_url"]
    try:
        short_url = encoded_urls.index(long_url)
    except:
        encoded_urls.append(long_url)
        short_url = encoded_urls.index(long_url)
    json_output   = {'short_url': f'{small_url_base+str(short_url)}'}
    return jsonify(json_output)

@app.route('/decode', methods=['POST'])
def decode_url ():
    """Decode Endpoint"""
    post_data      = request.get_json()
    short_url      = int(post_data["short_url"].replace(small_url_base, ''))
    try:
        long_url = encoded_urls[short_url]
    except:
        return
    json_output   = {'long_url': f'{long_url}'}
    return jsonify(json_output)

if __name__ == "__main__":
    app.run(debug=True)
