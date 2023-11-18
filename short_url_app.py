#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["2 per second"],
    storage_uri="memory://",
)

ENCODED_URLS = []
SMALL_URL_BASE = "http://smallurl/"


@app.errorhandler(429)
def rate_error(arg=""):
    """Rate Error Handler - Returns rate limit errors as JSON instead of the default HTML"""
    return jsonify({'error': 'Rate limit exceeded'}), 429


@app.route('/encode', methods=['POST'])
@limiter.limit("2 per second", error_message=rate_error)
def encode_url():
    """Encode Endpoint - Uses the ENCODED_URLS list index number as the URI to keep things simple"""
    post_data = request.get_json()
    try:
        long_url = post_data["long_url"]
    except KeyError:
        return jsonify({'error': 'Missing long_url parameter'}), 400

    try:
        short_url = ENCODED_URLS.index(long_url)
    except ValueError:
        ENCODED_URLS.append(long_url)
        short_url = ENCODED_URLS.index(long_url)

    json_output = {'short_url': f'{SMALL_URL_BASE + str(short_url)}'}
    return jsonify(json_output)


@app.route('/decode', methods=['POST'])
@limiter.limit("2 per second", error_message=rate_error)
def decode_url():
    """Decode Endpoint - Returns a long_url for the short_url if found"""
    post_data = request.get_json()
    try:
        short_url = int(post_data["short_url"].replace(SMALL_URL_BASE, ''))
    except KeyError:
        return jsonify({'error': 'Missing short_url parameter'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid short_url parameter'}), 400

    try:
        long_url = ENCODED_URLS[short_url]
    except IndexError:
        return jsonify({'error': 'Short URL not found'}), 404

    json_output = {'long_url': f'{long_url}'}
    return jsonify(json_output)

if __name__ == "__main__":
    app.run(debug=True)
