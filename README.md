
# Token Grabber Script

This is a Python script designed to gather Discord tokens stored locally on a system and send them to a specified Discord webhook. The script extracts tokens from various supported applications like Discord, Chrome, and other Chromium-based browsers. 

> **Disclaimer**: This script is intended for educational purposes only. Unauthorized use of this script without proper permission is prohibited and could violate the terms of service of various platforms. Always ensure you have proper permissions before using this tool.

## Features
- Extracts locally stored Discord tokens from multiple platforms and browsers.
- Decrypts the locally stored encrypted key to access the stored tokens.
- Sends the gathered tokens and user information to a specified Discord webhook.

## Supported Platforms
The script supports the following platforms and browsers:
- Discord
- Discord Canary
- Lightcord
- Discord PTB
- Opera
- Opera GX
- Chrome
- Brave
- Yandex

## Requirements
To run this script, the following Python libraries must be installed:

- `pycryptodome`
- `requests`
- `pywin32`

You can install these dependencies using:

```bash
pip install pycryptodome requests pywin32
```

## How It Works
1. **Token Extraction**: The script locates the encrypted tokens stored locally on the system for supported platforms.
2. **Decryption**: It decrypts these tokens using the system's master key to get the raw token values.
3. **Token Information**: The script then retrieves detailed information about each token, including username, email, and subscription details.
4. **Send to Webhook**: Finally, the extracted tokens and information are sent to a specified Discord webhook.


## Usage
1. Clone the repository or download the script.
2. Open the script in a text editor and replace `'WEBHOOK_HERE'` with your own Discord webhook URL.
3. Run the script using Python:

```bash
python script.py
```

4. The script will automatically gather tokens and send them to the specified webhook.

## Important Note
This script is intended for educational and ethical testing purposes only. Unauthorized use of this script is prohibited. Ensure you have proper permissions before running the script.

## Author
- **aselterik**

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

**Disclaimer**: This tool is intended for research purposes only. Unauthorized use without proper permissions is prohibited.
