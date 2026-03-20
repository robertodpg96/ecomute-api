import logging
import sys

# Create a custom logger
logger =  logging.getLogger('ecomute_logger')

# Set the lowest threshold for the logger itself
logger.setLevel(logging.DEBUG)

# Handler 1: Console (Standout Output)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO) # Ignore DEBUG messages in the console

# Handler 2: File (Warning and above)
file_handler = logging.FileHandler('ecomute.log')
file_handler.setLevel(logging.WARNING)  # Only save WARNINGS and above

# Formatting
formatter =  logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Attach everything together
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Activate
logger.addHandler(console_handler)
logger.addHandler(file_handler)