import os

# Fetch the API key from the environment
api_key = os.getenv("KANNAN")

if not api_key:
    print("KANNAN secret is NOT available.")
else:
    print("KANNAN secret is available.")
    print(f"API Key: {api_key}")  # For testing only; avoid printing secrets in production.
