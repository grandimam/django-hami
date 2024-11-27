# Protego Circuit Breaker for Django

Protego is a lightweight, in-memory circuit breaker for Django, designed to provide resilience in the face of service failures. It helps protect your application from failing requests by temporarily blocking calls to an external service when failures exceed a defined threshold.

## Features

- In-memory Circuit Breaker: Stores state in-memory, meaning it’s fast and easy to use.
- Flexible Configuration: Configure failure thresholds, reset timeouts, and retries for half-open state.
- Easy Integration: Integrates easily into your Django views using decorators.
- Dynamic Parameter Updates: Updates ProtegoClient configuration if the parameters change.
- Graceful Failure: Returns a 503 Service Unavailable response when the circuit is open.

## Installation

### Step 1: Add Protego to Your Project

First, add the protego.py file to your project. This file will contain the global registry that you can use across your project.

### Step 2: Create `protego.py` in Your Project

Create a protego.py file in your project directory (or any other location that suits you) to initialize the ProtegoRegistry. This file will ensure that the ProtegoRegistry is initialized only once during your Django application startup.

```
# protego.py

from protego.registry import ProtegoRegistry

# Initialize the registry once during the first import
protego = ProtegoRegistry()

```

### Step 3: Update settings.py

In your settings.py, ensure that the registry instance is available globally by importing it from the protego.py file.

```
# settings.py

from protego import protego  # Import the global registry
```

## Usage

You can now use the circuit breaker by decorating your views or functions with @registry.protect. This will apply the circuit breaker logic, allowing you to protect external service calls from failing repeatedly.

#### Example: Using @protego.protect in Views

You can use the circuit breaker by decorating your Django views with @protect. This will wrap the view function with circuit breaker logic, ensuring that the service fails gracefully when the circuit is open.

```
from django.http import JsonResponse
from protego import protego  # Import the global registry

# Example view using the circuit breaker
@protego.protect(failure_threshold=5, reset_timeout=30, half_open_retries=2)
def my_view(request):
    # Your business logic goes here
    return JsonResponse({"message": "Success!"})
```

### Explanation

- `failure_threshold (int)`: The number of failures before the circuit is opened (defaults to 3).
- `reset_timeout (int)`: The time (in seconds) before the circuit attempts to close again and allow requests (defaults to 60).
- `half_open_retries (int)`: The number of retries in half-open state to determine if the service should be considered recovered (defaults to 2).

## How It Works

1. **ProtegoRegistry**: The registry is responsible for managing ProtegoClient instances. When a client is requested, it checks whether the configuration has changed and updates the client accordingly.

2. **ProtegoClient**: This is the core object responsible for tracking the state of the circuit breaker. It keeps track of failure counts, manages the half-open state, and ensures that the circuit breaker logic is applied to requests.

### Circuit Breaker Logic:

- **Closed State**: The service is functioning normally. Requests are allowed.
- **Open State**: Too many failures have occurred, and requests are immediately rejected with a 503 error.
- **Half-Open State**: After the reset timeout, the circuit breaker enters a half-open state, where a few requests are allowed to test if the service is stable. If these requests succeed, the circuit is closed again.

## Conclusion

Protego provides a simple, powerful way to add resilience to your Django application with minimal setup and no external dependencies. By initializing the circuit breaker registry once and using it globally, you ensure that your application can protect external services from excessive failures while keeping the configuration clean and simple.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
