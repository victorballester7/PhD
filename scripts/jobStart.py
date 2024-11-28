import os
import socket
import sendMessage as sm  # Custom module to send messages

def notify_program_start():
    # Get current working directory and hostname
    current_directory = os.getcwd()
    hostname = socket.gethostname()

    # Construct the notification message
    message = f"✅ Program started. 🚀\n\n📂 Directory: `{current_directory}`\n💻 Hostname: `{hostname}`"

    # Send the message via sendMessage module (e.g., to Telegram)
    try:
        sm.send_telegram_message(message)
    except Exception as e:
        print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    notify_program_start()

