# Amazon Bedrock for Computer Use

This repository provides tools and scripts to demonstrate the use of Amazon Bedrock for computer operations, including S3 uploads and local system interactions. It is containerized using Docker for ease of deployment.

## Overview
The project includes modules to:
- Track computer usage and capture screenshots.
- Upload files and data to Amazon S3.
- Log operations for debugging and analysis.

## Folder Structure
```
├── app
│   ├── tool_use
│   │   ├── computer_use.py    # Tracks computer usage and handles screenshots
│   │   ├── s3_upload.py       # Handles S3 file uploads
│   │   └── __init__.py        # Package initialization
│   ├── requirements.txt       # Python dependencies
│   ├── logs                   # Stores application logs
│   ├── main.py                # Entry point for the application
│   └── tint2                  # Auxiliary tool (if applicable)
├── Dockerfile                 # Instructions to build the Docker container
├── entrypoint.sh              # Script to initialize the application
├── README.md                  # Project documentation
└── assets                     # Supplementary resources
```

## Key Components in the Dockerfile
The Dockerfile sets up the application in a containerized Ubuntu environment with:
- **UI tools:** `xvfb`, `x11vnc`, `firefox-esr`, `libreoffice`, etc.
- **Python environment:** `python3-pip`, `python3-tk`, and required dependencies from `requirements.txt`.
- **Libraries for screenshots and graphics:** `libxcb-*`, `gnome-screenshot`, `ffmpeg`.

### User Environment
A non-root user `computeruse` is created with the working directory set to `/home/computeruse`.

## Implementation Details

### `main.py`
The main script coordinates tool usage:
- **Logging:** Configures logging for operations.
- **Conversation Loop with Amazon Bedrock:**
  - Interacts with Amazon Bedrock to process user inputs using LLMs.
  - Sends user queries to Bedrock and parses responses to determine actions.
  - Executes steps such as triggering `ComputerUse` for local tasks or `S3Upload` for uploading files.
  - Continuously loops to handle multi-step interactions based on LLM responses.
- **Error Handling:** Logs errors during interactions and ensures the loop continues uninterrupted.

### `tool_use/computer_use.py`
- **Purpose:** Tracks system usage and captures screenshots.
- **Features:**
  - Uses `pyautogui` and `Xlib.display` for GUI interactions.
  - `SaveScreenshot` class captures and saves screenshots to a configurable directory.
  - Executes system commands to gather usage statistics or simulate user actions.
  - Includes safeguards to handle graphical environment availability (e.g., checking `DISPLAY` variable).

### `tool_use/s3_upload.py`
- **Purpose:** Manages file uploads to Amazon S3.
- **Features:**
  - `S3Upload` class provides methods for uploading files and objects.
  - Supports two primary operations:
    - **File Upload:** Uploads files from local storage to a specified S3 bucket.
    - **Memory Upload:** Directly uploads in-memory objects as S3 objects.
  - Defines a `TOOLSPEC` schema for specifying upload types and parameters.
  - Error handling ensures issues (e.g., network or permissions errors) are logged and retried when appropriate.

## How to Use
### Build and Run the Docker Container
1. Build the Docker image:
   ```bash
   podman build -t bedrock_computer_use .
   ```
2. Run the container:
   ```bash
   podman run -it --rm \
    -v ${PWD}/logs:/home/computeruse/logs \
    -e AWS_ACCESS_KEY_ID=$(aws --profile ${AWS_PROFILE} configure get aws_access_key_id) \
    -e AWS_SECRET_ACCESS_KEY=$(aws --profile ${AWS_PROFILE} configure get aws_secret_access_key) \
    -p 5900:5900 \
    bedrock_computer_use
   ```

   Runtime Configuration
   * Exposes port 5900 for VNC access
   * Mounts local logs directory
   * Requires AWS credentials as environment variables
   * Supports passing custom input commands

3. Enter the instruction after the input:
    ```bash
    Welcome to the Bedrock Interaction Script.
    Please enter your initial input:
    ```
4. You can connect to the view only VNC via port 5900.

### Example Usage

#### Get the last Singapore Car Ownership Entitlment (COE) bidding price

Prompt: 

```
Retrieve the latest Singapore COE bidding price and estimate the next bidding for Category A
```

Example output:

```
Bedrock: [{'text': 'Based on the latest COE bidding results for December 2024 2nd Open Bidding Exercise that ended on 18/12/2024, here are the details for Category A:\n\nCurrent Category A (Cars up to 1600cc & 130bhp):\n- Quota: 1,035\n- Quota Premium (QP): $96,000\n- Prevailing Quota Premium (PQP): $97,747\n\nFor projecting the next bidding, we need to consider several factors:\n\n1. Recent trend: The Category A COE price has shown some stability around the $95,000-$100,000 range\n\n2. Key factors that might influence the next bidding:\n- Quota for the next bidding exercise (if announced)\n- Seasonal demand (typically higher during the start of the year)\n- Recent policy changes or announcements\n- Economic conditions\n\nBased on these factors, we can project that the next Category A COE bidding price is likely to:\n- Remain relatively stable with a possible slight increase due to typical higher demand at the start of the year\n- Expected range: $96,000 - $98,000\n\nPlease note that this is a projection based on current available data and market conditions. Actual COE prices can be affected by various unforeseen factors and market dynamics.\n\nWould you like me to provide more specific analysis of any particular aspect of the COE bidding results or factors affecting the projection?'}]
```

![video](assets/computer_use.gif)

#### Find flights based on criteria and create a table

```
Find round-trip airfares from Singapore (SIN) to Bangkok (BKK) on Google Flights for the second week of February 2025, with arrival in Bangkok before 3 PM local time. Create a Markdown table in a text file listing the airfare, airline, date, and time. Upload the file to S3 bucket 654654616949-use1-media
```

## Contributions
Feel free to fork this repository and submit pull requests for new features or bug fixes.

## License
This project is licensed under the MIT License.

# References
* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
   * Alternatives are [xdotool](https://github.com/jordansissel/xdotool/tree/master)
* [Anthropic Computer Use](https://docs.anthropic.com/en/docs/build-with-claude/computer-use) and the [sample code on Github](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)
* [API doc for Bedrock converse](https://boto3.amazonaws.com/v1/documentation/api/1.35.8/reference/services/bedrock-runtime/client/converse.html)
