import sys
import sendMessage as sm
import os
import socket

def check_and_notify():
    NUMLINES = 40
    current_directory = os.getcwd()
    hostname = socket.gethostname() 
    try:
        with open("log.txt", "r") as log_file:
            log_content = log_file.read()


        if not log_content:  # If log.txt is empty
            message = f"✅ Program finished. 🏁 \n\n📂 Directory: `{current_directory}`\n💻 Hostname: `{hostname}`"
            try:
                with open("output.txt", "r") as output_file:
                    output_lines = output_file.readlines()[-NUMLINES:]  # Last 40 lines of output.txt
                details = "\n\n*Output:* \n```\n...\n" + "".join(output_lines) + "\n```"
            except Exception:
                details = f"\n\n No `output.txt` file found."
        else:  # If log.txt contains errors
            message = f"❌ Program encountered an error. \n\n📂 Directory: `{current_directory}`\n💻 Hostname: `{hostname}`"
            details = "\n\n*Error Log:* \n```\n" + log_content + "\n```"

        sm.send_telegram_message(message + details)
    except Exception as e:
        error_message = f"⚠️ An error occurred while checking log files. \n\n📂 Directory: `{current_directory}`\n💻 Hostname: `{hostname}` \n\n*Error:* `{e}`"
        sm.send_telegram_message(error_message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sendMessage.py '<folderWithFiles>'")
        sys.exit(1)

    # Check log and output files for success/failure message
    check_and_notify()


