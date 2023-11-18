#!/usr/bin/env python

import requests
import json
import unittest
import time
import argparse

BASE_URL = "http://127.0.0.1:5000"  # Default URL for app

def parse_arguments():
    parser = argparse.ArgumentParser(description='Test script for app endpoints')
    parser.add_argument('--base_url', default=BASE_URL, help='Base URL for the app')
    return parser.parse_args()

class TestAppEndpoints(unittest.TestCase):

    def test_encode_url(self):
        url = f"{BASE_URL}/encode"
        payload = {'long_url': 'http://example.com'}
        response = requests.post(url, json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('short_url', data)

    def test_encode_url_missing_parameter(self):
        url = f"{BASE_URL}/encode"
        payload = {}  # Missing 'long_url' parameter
        # We need to sleep over a half second for all these to not be rate limited
        time.sleep(1)
        response = requests.post(url, json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

    def test_decode_url(self):
        # Assumes /encode endpoint worked
        encode_url = f"{BASE_URL}/encode"
        encode_payload = {'long_url': 'http://example.com'}
        encode_response = requests.post(encode_url, json=encode_payload)
        encode_data = encode_response.json()

        short_url = encode_data['short_url']
        decode_url = f"{BASE_URL}/decode"
        payload = {'short_url': short_url}
        time.sleep(1)
        response = requests.post(decode_url, json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('long_url', data)

    def test_decode_url_missing_parameter(self):
        url = f"{BASE_URL}/decode"
        payload = {}  # Missing 'short_url' parameter
        time.sleep(1)
        response = requests.post(url, json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

    def test_decode_url_invalid_parameter(self):
        url = f"{BASE_URL}/decode"
        payload = {'short_url': 'invalid_short_url'}
        time.sleep(1)
        response = requests.post(url, json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

    def test_decode_url_not_found(self):
        url = f"{BASE_URL}/decode"
        payload = {'short_url': 'http://smallurl/999'}  # Assuming this doesn't exist
        time.sleep(1)
        response = requests.post(url, json=payload)

        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('error', data)

    def test_encode_url_respect_rate_limit(self):
        url = f"{BASE_URL}/encode"
        payload = {'long_url': 'http://example.com'}

        # Make 3 requests within 1 second to trigger rate limit
        for _ in range(3):
            response = requests.post(url, json=payload)
            self.assertIn(response.status_code, [200, 429])  # Should either succeed or be rate-limited

        # Make another request which should fail due to rate limit
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 429)
    
    def test_decode_url_respect_rate_limit(self):
        # Wait a full second after previous test
        time.sleep(1)
        encode_url = f"{BASE_URL}/encode"
        encode_payload = {'long_url': 'http://example.com'}
        encode_response = requests.post(encode_url, json=encode_payload)
        encode_data = encode_response.json()

        short_url = encode_data['short_url']
        url = f"{BASE_URL}/decode"

        # Make 3 requests within 1 second to trigger rate limit
        for _ in range(3):
            payload = {'short_url': short_url}
            response = requests.post(url, json=payload)
            self.assertIn(response.status_code, [200, 429])  # Should either succeed or be rate-limited

        # Make another request which should fail due to rate limit
        payload = {'short_url': short_url}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 429)


if __name__ == '__main__':
    args = parse_arguments()
    BASE_URL = args.base_url  # Update the global BASE_URL

    unittest.main(argv=['first-arg-is-ignored'], exit=False)

