import http.client
import json
import sys
from urllib.parse import urlencode

TOKEN = '7706610430:AAGPonBRvtp_PM5IefGp8JnMFU51u0RVZYg'
CHAT_ID = '2016492065'

def send_telegram_message(text):
    print("Sending message to Telegram...")
    try:
        # Define the API endpoint and parameters
        host = "api.telegram.org"
        endpoint = f"/bot{TOKEN}/sendMessage"
        params = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }

        # Encode the parameters
        body = urlencode(params)

        # Create an HTTP connection and send the POST request
        conn = http.client.HTTPSConnection(host)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn.request("POST", endpoint, body, headers)

        # Get the response
        response = conn.getresponse()
        if response.status == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.status} {response.reason}")
            print(f"Response: {response.read().decode()}")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

def check_and_notify():
    NUMLINES = 40
    try:
        with open("log.txt", "r") as log_file:
            log_content = log_file.read()

        if not log_content:  # If log.txt is empty
            message = "✅ Program finished."
            try:
                with open("output.txt", "r") as output_file:
                    output_lines = output_file.readlines()[-NUMLINES:]  # Last 40 lines of output.txt
                details = "\n\n*Output:* \n```\n...\n" + "".join(output_lines) + "\n```"
            except Exception:
                details = f"\n\n No `output.txt` file found."
        else:  # If log.txt contains errors
            message = "❌ Program encountered an error."
            details = "\n\n*Error Log:* \n```\n" + log_content + "\n```"

        send_telegram_message(message + details)
    except Exception as e:
        error_message = f"An error occurred while checking log files: {e}"
        send_telegram_message(error_message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sendMessage.py '<folderWithFiles>'")
        sys.exit(1)

    # Check log and output files for success/failure message
    check_and_notify()

