from django.http import HttpResponseForbidden
from django.conf import settings
import re

class SecurityMiddleware:
    """
    Additional security middleware to protect against common attacks
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Block suspicious request methods
        if request.method not in ['GET', 'POST', 'HEAD']:
            return HttpResponseForbidden('Method not allowed')

        # Basic SQL injection protection (additional layer)
        sql_patterns = [
            r';\s*--',  # SQL comment
            r';\s*/\*',  # SQL comment block
            r'union\s+select',  # Union select
            r'/\*.*\*/',  # Comment blocks
        ]

        # Check GET and POST parameters for suspicious patterns
        for key, value in request.GET.items():
            if isinstance(value, str):
                for pattern in sql_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return HttpResponseForbidden('Invalid request')

        for key, value in request.POST.items():
            if isinstance(value, str):
                for pattern in sql_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return HttpResponseForbidden('Invalid request')

        # Check User-Agent for suspicious patterns
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if any(suspicious in user_agent.lower() for suspicious in ['sqlmap', 'nmap', 'masscan']):
            return HttpResponseForbidden('Access denied')

        response = self.get_response(request)
        return response