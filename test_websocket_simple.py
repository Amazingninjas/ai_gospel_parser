#!/usr/bin/env python3
"""
Simple WebSocket test for AI chat.
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/api/chat/stream"

    try:
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to WebSocket")

            # Send a test message
            message = {
                "message": "What does agape mean?",
                "verse_reference": None,
                "conversation_history": [],
                "include_lexicon": True
            }

            print(f"→ Sending: {message['message']}")
            await websocket.send(json.dumps(message))

            # Receive and print responses
            response_text = ""
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    data = json.loads(response)

                    if data.get("error"):
                        print(f"⚠ Error: {data['error']}")
                        break

                    chunk = data.get("chunk", "")
                    if chunk:
                        response_text += chunk
                        print(chunk, end="", flush=True)

                    if data.get("done"):
                        print("\n✓ Done")
                        break

                except asyncio.TimeoutError:
                    print("\n⚠ Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"\n⚠ Error receiving: {e}")
                    break

            print(f"\nFull response ({len(response_text)} chars):")
            print(response_text)

    except Exception as e:
        print(f"✗ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
