import paho.mqtt.client as mqtt
import time
import json
import os

from games import Game

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback function for when the client successfully connects to the MQTT broker.
    """
    print(f"🔵 on_connect called with reason_code: {reason_code}")
    if reason_code == 0:
        print("✅ Successfully connected to MQTT broker")
    else:
        print(f"❌ Connection failed with code: {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    """
    Callback function for when the client disconnects from the MQTT broker.
    """
    print(f"🟠 on_disconnect called with reason_code: {reason_code}")

def test_connection():
    """
    Test the connection to the MQTT broker.
    """
    print("Starting MQTT connection test...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    connected = False
    
    try:
        print("🔄 Attempting to connect to MQTT broker...")
        client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')), 60)
        
        # Start network loop
        client.loop_start()
        
        # Wait for connection
        print("⏳ Waiting for connection... (max 5 seconds)")
        for i in range(50):  # 50 * 0.1s = 5s
            if client.is_connected():
                print("✅ Client reports as connected!")
                break
            time.sleep(0.1)

            connected = True
        else:
            print("❌ Connection timeout - broker not responding")
        
        # Clean up
        client.loop_stop()

        return connected
        
    except Exception as e:
        print(f"❌ Exception: {e}")
    finally:
        client.disconnect()
        print("Test completed")

def listen_for_code_updates():
    """
    Listen for new codes on the MQTT broker.
    """
    def on_message(client, userdata, msg):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{current_time}] - Received message on topic {msg.topic}: {msg.payload.decode()}")
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')))
        client.subscribe("gamecodes/#")
        print("Listening for messages on topic 'gamecodes/#'. Press Ctrl+C to exit...")
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping listener...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()

def broadcast_new_code(codes, game):
    """
    Broadcast a new code to the MQTT broker.
    """

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')))
    client.publish("gamecodes/" + game, json.dumps(codes))
    client.disconnect()

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
        print('Raw execution prohibited...')    