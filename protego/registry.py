from django.http import JsonResponse
from protego.client import ProtegoClient

class ProtegoRegistry:
    def __init__(self):
        self._registry = {}

    def get_or_create_client(self, key, failure_threshold=3, reset_timeout=60, half_open_retries=2):
        config = {
            "failure_threshold": failure_threshold,
            "reset_timeout": reset_timeout,
            "half_open_retries": half_open_retries
        }
        if key in self._registry:
            client = self._registry[key]
            if client.config != config:
                self._registry[key] = ProtegoClient()
        else:
            self._registry[key] = ProtegoClient()
        return self._registry[key]

    
    def protect(self, failure_threshold=None, reset_timeout=None, half_open_retries=None):
        """
        Decorator method to wrap views with the circuit breaker logic.
        """
        def decorator(func):
            def wrapped_view(request, *args, **kwargs):
                client = self.get_or_create_client(
                    key=func.__name__,
                    failure_threshold=failure_threshold,
                    reset_timeout=reset_timeout,
                    half_open_retries=half_open_retries
                )
                try:
                    return client.call(func, request, *args, **kwargs)
                except Exception:
                    return JsonResponse({"message": "Service unavailable"}, status=503)

            return wrapped_view
        return decorator
