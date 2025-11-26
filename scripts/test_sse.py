import asyncio
import httpx
import json
import sys

async def test_sse():
    url = "http://localhost:8000/assist"
    payload = {"prompt": "https://polymarket.com/event/will-bitcoin-hit-100k-in-2024", "stream": True}
    
    print(f"Connecting to {url} with payload: {payload}")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                print(await response.read())
                return

            print("Connected. Listening for events...")
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    try:
                        json_data = json.loads(data)
                        print(f"Received event: {json.dumps(json_data, indent=2)}")
                        if json_data.get("type") == "ANALYSIS_MARKDOWN":
                             # Just print a summary for markdown chunks to avoid clutter
                             print(f"Markdown chunk received: {len(json_data.get('chunk', ''))} chars")
                    except json.JSONDecodeError:
                        print(f"Received raw data: {data}")
                elif line.startswith("event: "):
                    print(f"Event type: {line[7:]}")

if __name__ == "__main__":
    try:
        asyncio.run(test_sse())
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
