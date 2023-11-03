import logging

class CustomLoggingFormatter(logging.Formatter):
    def format(self, record):
        # Apply styling to the log message
        message = f'<span style="background-color: yellow; color: red;">{record.getMessage()}</span>'
        record.msg = message
        return super().format(record)