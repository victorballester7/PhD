import sys
import sendMessage as sm
import os
import socket


def check_and_notify(job_id):
    NUMLINES_log = 20
    NUMLINES_output = 40
    output_file = "output.txt"
    log_file = "log.txt"

    current_directory = os.getcwd()
    hostname = socket.gethostname()
    try:
        with open(log_file, "r") as log_file:
            log_content = log_file.readlines()[
                -NUMLINES_log:
            ]  # Last 40 lines of log.txt

        # Check if 'timeout' word is present in log.txt
        timeout = any("timeout" in line for line in log_content)
        cancelled = any("killed intentionally" in line for line in log_content)

        if not log_content:  # If log.txt is empty
            message = f"✅ Program finished successfully. 🏁 \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"
            try:
                with open(output_file, "r") as output_file:
                    output_lines = output_file.readlines()[
                        -NUMLINES_output:
                    ]  # Last 40 lines of output.txt
                details = "\n\n*Output:* \n```\n...\n" + "".join(output_lines) + "\n```"
            except Exception:
                details = f"\n\n No `{output_file}` file found."
        elif timeout and not cancelled:  # If log.txt containes timeout message
            message = f"⚠️ Program timed out. ⏳ \n\n📂 *Directory*: `{current_directory}`\n💻 *Hostname*: `{hostname}`\n🆔 *Job ID*: `{job_id}`"
            try:
                with open(output_file, "r") as output_file:
                    output_lines = output_file.readlines()[
                        -NUMLINES_output:
                    ]  # Last 40 lines of output.txt
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
                with open(output_file, "r") as output_file:
                    output_lines = output_file.readlines()[
                        -NUMLINES_output:
                    ]  # Last 40 lines of output.txt
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
