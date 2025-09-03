# test_gateway.py
import requests
import json
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import sys

print("Starting gateway test...")

try:
    # Load configuration
    print("Loading configuration...")
    with open('gateway_config.json', 'r') as f:
        config = json.load(f)
    print("✓ Configuration loaded")
    
    print("Creating client...")
    client = GatewayClient(region_name="us-east-1")
    print("✓ Client created")
    
    # Get access token
    print("Getting access token...")
    try:
        access_token = client.get_access_token_for_cognito(config['cognito_info']['client_info'])
        print(f"✓ Access token obtained: {access_token[:20]}...")
    except Exception as e:
        print(f"❌ Failed to get access token: {e}")
        sys.exit(1)
    
    # Test listing tools
    gateway_url = config['gateway_url']
    print(f"\nTesting gateway at: {gateway_url}")
    
    print("\n1. Testing tools/list...")
    try:
        response = requests.post(
            gateway_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "jsonrpc": "2.0",
                "id": "test-list",
                "method": "tools/list",
                "params": {}
            },
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print("Available tools:")
        if response.status_code == 200:
            tools = response.json()
            print(json.dumps(tools, indent=2))
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print("\n2. Testing get_weather tool...")
    try:
        response = requests.post(
            gateway_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "jsonrpc": "2.0",
                "id": "test-weather",
                "method": "tools/call",
                "params": {
                    "name": "WeatherAndTimeTools___get_weather",
                    "arguments": {
                        "location": "Seattle"
                    }
                }
            },
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print("Weather response:")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print("\n3. Testing get_time tool...")
    try:
        response = requests.post(
            gateway_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "jsonrpc": "2.0",
                "id": "test-time",
                "method": "tools/call",
                "params": {
                    "name": "WeatherAndTimeTools___get_time",
                    "arguments": {
                        "timezone": "America/New_York"
                    }
                }
            },
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print("Time response:")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

except FileNotFoundError:
    print("❌ gateway_config.json not found")
    print("Please run create_gateway_with_targets.py first")
except json.JSONDecodeError:
    print("❌ Invalid JSON in gateway_config.json")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed.")
