"""Small helpers: IP checks, cfg parsing, HMAC verification, etc."""

import re
import ipaddress
import hmac
import hashlib


def is_valid_ip(ip_string):
    """Check if a string is a valid IP address."""
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def parse_config(filepath):
    """Parse a configuration file into a dictionary."""
    config = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def compute_hmac(key, message, digestmod='sha256'):
    """
    Compute HMAC for a message using a key.
    
    Args:
        key: Secret key (string or bytes)
        message: Message to authenticate (string or bytes)
        digestmod: Hash algorithm to use (default: sha256)
    
    Returns:
        Hexadecimal digest string
    """
    # Convert to bytes if needed
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # Compute HMAC
    h = hmac.new(key, message, digestmod=digestmod)
    return h.hexdigest()


def verify_hmac(key, message, expected_hmac, digestmod='sha256'):
    """
    Verify HMAC for a message.
    
    Args:
        key: Secret key (string or bytes)
        message: Message to authenticate (string or bytes)
        expected_hmac: Expected HMAC digest (hex string)
        digestmod: Hash algorithm to use (default: sha256)
    
    Returns:
        True if HMAC matches, False otherwise
    """
    computed = compute_hmac(key, message, digestmod)
    return hmac.compare_digest(computed, expected_hmac)

