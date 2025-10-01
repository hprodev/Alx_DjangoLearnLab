#!/usr/bin/env python3
"""
Security Testing Script for Django HTTPS Implementation
"""

import requests
import ssl
import socket
from urllib.parse import urljoin

def test_https_redirect(base_url):
    """Test if HTTP redirects to HTTPS"""
    try:
        http_url = base_url.replace('https://', 'http://')
        response = requests.get(http_url, allow_redirects=False)
        
        if response.status_code in [301, 302]:
            redirect_url = response.headers.get('Location', '')
            if redirect_url.startswith('https://'):
                print("✅ HTTP to HTTPS redirect: PASS")
                return True
        
        print("❌ HTTP to HTTPS redirect: FAIL")
        return False
        
    except Exception as e:
        print(f"❌ HTTP redirect test failed: {e}")
        return False

def test_security_headers(base_url):
    """Test security headers"""
    try:
        response = requests.get(base_url)
        headers = response.headers
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS header',
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
            'X-XSS-Protection': 'XSS protection',
            'Referrer-Policy': 'Referrer policy'
        }
        
        print("Security Headers Test:")
        for header, description in security_headers.items():
            if header in headers:
                print(f"✅ {description}: {headers[header]}")
            else:
                print(f"❌ {description}: Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Security headers test failed: {e}")
        return False

def test_ssl_configuration(hostname):
    """Test SSL/TLS configuration"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"✅ SSL Certificate: {ssock.version()}")
                cert = ssock.getpeercert()
                print(f"✅ Certificate Subject: {cert['subject']}")
                print(f"✅ Certificate Issuer: {cert['issuer']}")
        return True
        
    except Exception as e:
        print(f"❌ SSL test failed: {e}")
        return False

def test_csrf_protection(base_url):
    """Test CSRF protection"""
    try:
        # Try to make a POST request without CSRF token
        response = requests.post(urljoin(base_url, '/admin/login/'))
        
        if response.status_code == 403:
            print("✅ CSRF Protection: PASS")
            return True
        else:
            print("❌ CSRF Protection: May not be properly configured")
            return False
            
    except Exception as e:
        print(f"❌ CSRF test failed: {e}")
        return False

if __name__ == "__main__":
    # Update with your domain
    BASE_URL = "https://yourdomain.com"
    HOSTNAME = "yourdomain.com"
    
    print("Django HTTPS Security Test Suite")
    print("=" * 40)
    
    test_https_redirect(BASE_URL)
    test_security_headers(BASE_URL)
    test_ssl_configuration(HOSTNAME)
    test_csrf_protection(BASE_URL)
    
    print("\nTest completed!")
    print("For comprehensive testing, also check:")
    print("- https://www.ssllabs.com/ssltest/")
    print("- https://securityheaders.com/")