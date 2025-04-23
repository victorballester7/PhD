import sys
import sendMessage as sm
import os
import socket


def get_last_lines(file):
    NUMLINES = 40
    MAX_CHAR_TELEGRAM_MSG = 4096
    last_lines = []
    with open(file, "r") as f:
        lines = f.readlines()
        num_characters = MAX_CHAR_TELEGRAM_MSG + 1
        scale = 0.8
        while num_characters > MAX_CHAR_TELEGRAM_MSG:
            last_lines = lines[-int(NUMLINES * scale) :]
            num_characters = sum(len(line) for line in last_lines)  # Count characters
            scale *= scale  # Adjust scale iteratively

    return last_lines  # Return the selected lines

    

def check_and_notify(job_id):
    output_file = "output.txt"
    log_file = "log.txt"

    current_directory = os.getcwd()
    hostname = socket.gethostname()
    try:
        log_content = get_last_lines(log_file)        # Check if 'timeout' word is present in log.txt
        timeout = any("timeout" in line for line in log_content)
        cancelled = any("killed intentionally" in line for line in log_content)

        if not log_content:  # If log.txt is empty
            message = f"✅ Program finished successfully. 🏁 \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"
            try:
                output_lines = get_last_lines(output_file)
                details = "\n\n*Output:* \n```\n...\n" + "".join(output_lines) + "\n```"
            except Exception:
                details = f"\n\n No `{output_file}` file found."
        elif timeout and not cancelled:  # If log.txt containes timeout message
            message = f"⚠️ Program timed out. ⏳ \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"
            try:
                output_lines = get_last_lines(output_file)
                details = (
                    "\n\n*Output so far:* \n```\n...\n"
                    + "".join(output_lines)
                    + "\n```"
                )
            except Exception:
                details = f"\n\n No `{output_file}` file found."
        elif not timeout and cancelled:  # If log.txt contains errors
            message = f"☢️ Program was cancelled. 🙅 \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"
            try:
                output_lines = get_last_lines(output_file)
                details = (
                    "\n\n*Output before cancellation:* \n```\n...\n"
                    + "".join(output_lines)
                    + "\n```"
                )
            except Exception:
                details = f"\n\n No `{output_file}` file found."

        else:  # If log.txt contains errors
            message = f"❌ Program encountered an error. ⛔ \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"
            details = "\n\n*Error Log:* \n```\n" + "".join(log_content) + "\n```"

        try:
            sm.send_telegram_message(message + details)
        except Exception as e:
            with open("log.txt", "a") as log_file:
                log_file.write(f"Failed to send notification: {e}")
    except Exception as e:
        error_message = f"⚠️ An error occurred while checking log files. \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}` \n\n*Error:* `{e}`"
        try:
            sm.send_telegram_message(error_message)
        except Exception as e:
            with open("log.txt", "a") as log_file:
                log_file.write(f"Failed to send notification: {e}")


if __name__ == "__main__":
    job_id = sys.argv[1]
    # Check log and output files for success/failure message
    check_and_notify(job_id)
