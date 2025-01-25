import os

# Path to the root directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the resources directory where databases and photos are stored
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')

# Path to the DB folder inside resources
DB_DIR = os.path.join(RESOURCES_DIR, 'DB')

# Path to the folder for storing photos
PHOTOS_DIR = os.path.join(RESOURCES_DIR, 'photos')

# Path to the temporary folder
TEMP_DIR = os.path.join(RESOURCES_DIR, 'temp')

# Path to the models directory
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Define the environment variable for the admin bot token
TOKEN_ENV_VAR = "TELEGRAM_BOT_TOKEN_CHECKER"

# Attempt to retrieve the token from the environment variable
token = os.getenv(TOKEN_ENV_VAR)

if not token:
    # If the token is not found in the environment, attempt to load it from a text file
    try:
        token_file_path = os.path.join(BASE_DIR, 'token.txt')
        with open(token_file_path, 'r') as f:
            # Parse the file for a line starting with "checker="
            for line in f:
                if line.startswith("checker="):
                    token = line.split('=')[1].strip()
                    break
        if not token:
            raise ValueError("The admin bot token was not found in the file.")
    except FileNotFoundError:
        raise ValueError("The admin bot token file was not found.")
