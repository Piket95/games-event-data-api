import paho.mqtt.client as mqtt
import time
import json
import os

from helpers.games import Game
from helpers.log import Log
import database.database as db

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback function for when the client successfully connects to the MQTT broker.
    """
    Log()(f"🔵 on_connect called with reason_code: {reason_code}")
    if reason_code == 0:
        Log()("✅ Successfully connected to MQTT broker")
    else:
        Log()(f"❌ Connection failed with code: {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    """
    Callback function for when the client disconnects from the MQTT broker.
    """
    Log()(f"🟠 on_disconnect called with reason_code: {reason_code}")

def test_connection() -> bool:
    """
    Test the connection to the MQTT broker.
    """
    Log()("Starting MQTT connection test...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    try:
        connected = False
        Log()("🔄 Attempting to connect to MQTT broker...")
        client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')), 60)
        
        # Start network loop
        client.loop_start()
        
        # Wait for connection
        Log()("⏳ Waiting for connection... (max 5 seconds)")
        for i in range(50):  # 50 * 0.1s = 5s
            if client.is_connected():
                Log()("✅ Client reports as connected!")
                connected = True
                break
            time.sleep(0.1)
        else:
            Log()("❌ Connection timeout - broker not responding")
        
        # Clean up
        client.loop_stop()

        return connected
    except Exception as e:
        return False
    finally:
        client.disconnect()
        # Log()("Test completed")

def listen_for_code_updates():
    """
    Listen for new codes on the MQTT broker.
    """
    def on_message(client, userdata, msg):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Log()(f"[{current_time}] - Received message on topic {msg.topic}: {msg.payload.decode()}")
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')))
        client.subscribe("gamecodes/#")
        Log()("Listening for messages on topic 'gamecodes/#'. Press Ctrl+C to exit...")
        client.loop_forever()
    except KeyboardInterrupt:
        Log()("Stopping listener...")
    except Exception as e:
        Log().error(f"Error: {e}")
    finally:
        client.disconnect()

def broadcast_new_code(codes, game):
    """
    Broadcast a new code to the MQTT broker.
    """

    # test the connection to the broker to get a notification at the terminal if the connection fails on worst case, so the hoster is informed at least
    if not test_connection():
        Log().error('Could not connect to MQTT broker. Is the server down? Aborting broadcast...')
        return

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')))
    client.publish("gamecodes/" + game, json.dumps(codes))
    client.disconnect()
    
    db.set_code_broadcasted(codes, game)

# for testing and documentation purposes only. Not meant to be used in production
if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse

    load_dotenv()
    
    parser = argparse.ArgumentParser(description='MQTT Code Broadcaster/Listener')
    parser.add_argument('--listen', action='store_true', help='Listen for incoming codes instead of broadcasting')
    parser.add_argument('--send-test-code', action='store_true', help='Send a testcode to MQTT to test the connection and functionallity')
    args = parser.parse_args()
    
    if args.listen:
        listen_for_code_updates()
    elif args.send_test_code:
        broadcast_new_code("DEVTESTCODE", Game.WUTHERING_WAVES.value)
    else:
        print('\033[91mRaw execution prohibited...\033[0m')
        parser.print_help()