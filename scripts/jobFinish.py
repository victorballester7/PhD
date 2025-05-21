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
            last_lines = lines[-int(NUMLINES * scale):]
            num_characters = sum(len(line) for line in last_lines)
            scale *= scale
    return last_lines

def check_and_notify(job_id):
    output_file = "output.txt"
    log_file = "log.txt"

    current_directory = os.getcwd()
    hostname = socket.gethostname()

    try:
        log_content = get_last_lines(log_file)
        timeout = any("timeout" in line for line in log_content)
        cancelled = any("killed intentionally" in line for line in log_content)
        if not log_content:
            message = (
                "✅ <b>Program finished successfully</b> 🏁\n\n"
                f"📂 <b>Directory</b>: <code>{current_directory}</code>\n"
                f"💻 <b>Hostname</b>: <code>{hostname}</code>\n"
                f"🆔 <b>Job ID</b>: <code>{job_id}</code>"
            )
            try:
                output_lines = get_last_lines(output_file)
                details = (
                    "\n\n<b>Output:</b>\n<blockquote expandable>...\n" +
                    "".join(output_lines) +
                    "</blockquote>"
                )
            except Exception:
                details = f"\n\n No <code>{output_file}</code> file found."
        elif timeout and not cancelled:
            message = (
                "⚠️ <b>Program timed out</b> ⏳\n\n"
                f"📂 <b>Directory</b>: <code>{current_directory}</code>\n"
                f"💻 <b>Hostname</b>: <code>{hostname}</code>\n"
                f"🆔 <b>Job ID</b>: <code>{job_id}</code>"
            )
            try:
                output_lines = get_last_lines(output_file)
                details = (
                    "\n\n<b>Output so far:</b>\n<blockquote expandable>...\n" +
                    "".join(output_lines) +
                    "</blockquote>"
                )
            except Exception:
                details = f"\n\n No <code>{output_file}</code> file found."
        elif not timeout and cancelled:
            message = (
                "☢️ <b>Program was cancelled</b> 🙅\n\n"
                f"📂 <b>Directory</b>: <code>{current_directory}</code>\n"
                f"💻 <b>Hostname</b>: <code>{hostname}</code>\n"
                f"🆔 <b>Job ID</b>: <code>{job_id}</code>"
            )
            try:
                output_lines = get_last_lines(output_file)
                details = (
                    "\n\n<b>Output before cancellation:</b>\n<blockquote expandable>...\n" +
                    "".join(output_lines) +
                    "</blockquote>"
                )
            except Exception:
                details = f"\n\n No <code>{output_file}</code> file found."
        else:
            message = (
                "❌ <b>Program encountered an error</b> ⛔\n\n"
                f"📂 <b>Directory</b>: <code>{current_directory}</code>\n"
                f"💻 <b>Hostname</b>: <code>{hostname}</code>\n"
                f"🆔 <b>Job ID</b>: <code>{job_id}</code>"
            )
            details = "\n\n<b>Error Log:</b>\n<blockquote expandable>" + "".join(log_content) + "</blockquote>"

        try:
            sm.send_telegram_message(message, details)
        except Exception as e:
            with open("log.txt", "a") as log_file:
                log_file.write(f"Failed to send notification: {e}")
    except Exception as e:
        error_message = (
            "⚠️ <b>An error occurred while checking log files.</b>\n\n"
            f"📂 <b>Directory</b>: <code>{current_directory}</code>\n"
            f"💻 <b>Hostname</b>: <code>{hostname}</code>\n"
            f"🆔 <b>Job ID</b>: <code>{job_id}</code>\n\n"
            f"<b>Error:</b> <code>{e}</code>"
        )
        try:
            sm.send_telegram_message(error_message)
        except Exception as e:
            with open("log.txt", "a") as log_file:
                log_file.write(f"Failed to send notification: {e}")

if __name__ == "__main__":
    job_id = sys.argv[1]
    check_and_notify(job_id)

