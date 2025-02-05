import os
import socket
import sendMessage as sm  # Custom module to send messages
import sys

def notify_program_start(job_id):
    # Get current working directory and hostname
    current_directory = os.getcwd()
    hostname = socket.gethostname()

    # Construct the notification message
    message = f"✅ Program started. 🚀\n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"

    # Send the message via sendMessage module (e.g., to Telegram)
    try:
        sm.send_telegram_message(message)
    except Exception as e:
        print(f"Failed to send notification: {e}")

if __name__ == "__main__":
    # get the first argument from the command line
    job_id = sys.argv[1]

    notify_program_start(job_id)

