#!/usr/bin/env python3
"""
Script to automatically generate Alpha Vantage API keys.
This script provides a Flask server with endpoints to generate and manage API keys.
"""

import os
import random
import string
import logging
from datetime import datetime
from typing import Tuple, Optional

from flask import Flask, jsonify
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def generate_random_email() -> str:
    """Generate a random email for API key registration."""
    username_length = random.randint(6, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    year = random.randint(1980, 2000)
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    domain = random.choice(domains)
    return f"{username}+{year}@{domain}"

def generate_api_key() -> Tuple[Optional[str], Optional[str]]:
    """
    Generate a new Alpha Vantage API key.
    
    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing (api_key, error_message).
        If successful, api_key will contain the key and error will be None.
        If failed, api_key will be None and error will contain the error message.
    """
    url = "https://www.alphavantage.co/create_post/"
    email = generate_random_email()
    
    logger.info("Attempting to generate new API key...")
    logger.debug("Using email: %s", email)
    
    # Get CSRF token first
    try:
        session = requests.Session()
        support_url = "https://www.alphavantage.co/support/"
        session.get(support_url)
        csrf_token = session.cookies.get('csrftoken')
        logger.debug("CSRF token: %s", csrf_token)
        
        if not csrf_token:
            logger.error("Failed to get CSRF token")
            return None, "Failed to get CSRF token"
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.alphavantage.co',
            'referer': 'https://www.alphavantage.co/support/',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': csrf_token
        }
        
        data = {
            'csrfmiddlewaretoken': csrf_token,
            'first_text': 'deprecated',
            'last_text': 'deprecated',
            'occupation_text': 'Investor',
            'organization_text': 'Trading Corp',
            'email_text': email
        }
        
        response = session.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()
        
        if 'text' in response_data:
            # Try different patterns to extract API key
            patterns = [
                'API key: ',
                'Your API key is: ',
                'Your dedicated access key is: ',
                'access key: '
            ]
            
            for pattern in patterns:
                if pattern in response_data['text']:
                    api_key = response_data['text'].split(pattern)[1].split('.')[0].strip()
                    logger.info("Successfully generated API key")
                    return api_key, None
            
            logger.error("Could not find API key in response")
            return None, "Could not find API key in response"
        else:
            logger.error("Invalid response format from Alpha Vantage")
            return None, "Invalid response format"
            
    except requests.exceptions.RequestException as e:
        logger.error("Network error: %s", str(e))
        return None, f"Network error: {str(e)}"
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return None, f"Unexpected error: {str(e)}"

@app.route('/api/token', methods=['GET'])
def get_token():
    """API endpoint to get a new Alpha Vantage API key."""
    api_key, error = generate_api_key()
    
    if api_key:
        response = {
            'success': True,
            'api_key': api_key,
            'generated_at': datetime.utcnow().isoformat(),
            'message': 'API key generated successfully'
        }
        logger.info("API key generated successfully")
        return jsonify(response)
    else:
        response = {
            'success': False,
            'error': error,
            'message': 'Failed to generate API key'
        }
        logger.error("Failed to generate API key: %s", error)
        return jsonify(response), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7785))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info("Starting Alpha Vantage API Key Generator server...")
    logger.info("Port: %d", port)
    logger.info("Debug mode: %s", "enabled" if debug else "disabled")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 