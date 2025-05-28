# Mem0 Web UI

This is a simple web UI for interacting with the Mem0 AI library, allowing users to add, search, retrieve, and delete memories associated with specific user IDs.

## Project Structure

```
mem0_web_ui/
├── .venv/                   # Python virtual environment (should be in .gitignore)
├── app.py                   # Main Flask application
├── templates/
│   └── index.html           # Frontend HTML
├── README.md                # This file
└── .gitignore               # Specifies intentionally untracked files
```

## Setup and Running

1.  **Navigate to the `mem0_web_ui` directory:**
    ```bash
    cd mem0_web_ui
    ```

2.  **Create and Activate Python Virtual Environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    # Create the virtual environment (e.g., named .venv)
    python3 -m venv .venv 
    # Activate it (on macOS/Linux)
    source .venv/bin/activate
    # On Windows, use: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install the necessary Python libraries.
    ```bash
    pip install Flask mem0ai
    # Consider creating a requirements.txt file for larger projects:
    # pip freeze > requirements.txt 
    # then install with: pip install -r requirements.txt
    ```

4.  **Configure Flask Application:**
    Set the `FLASK_APP` environment variable.
    ```bash
    export FLASK_APP=app.py
    # For Windows (cmd.exe): set FLASK_APP=app.py
    # For Windows (PowerShell): $env:FLASK_APP="app.py"
    ```

5.  **Run the Flask Development Server:**
    You can specify a port if needed (e.g., 8087).
    ```bash
    flask run --host=0.0.0.0 --port=8087
    # Or simply 'flask run' to use the default port 5000
    ```
    The application will be accessible at `http://127.0.0.1:PORT_NUMBER/` (e.g., `http://127.0.0.1:8087/`).

## Current Operating Mode: Stubbed API Responses

**IMPORTANT:** By default, this application runs in a **stubbed API mode**. This means the backend API endpoints (`/api/memory/*`) return predefined, mock data instead of interacting with a live Mem0 instance. This mode is designed for:
*   Easy frontend development and testing of the UI flow.
*   Running the application without needing a live Mem0 backend or API keys (like `OPENAI_API_KEY`).

The actual calls to the `mem0_instance` within `mem0_web_ui/app.py` are commented out.

### Switching to Live Mem0 Operations

To connect the web UI to a real Mem0 backend:

1.  **Modify `app.py`:**
    *   Open `mem0_web_ui/app.py`.
    *   In each of the API endpoint functions (`add_memory`, `search_memory`, `get_all_memories`, `delete_memory_endpoint`):
        *   Comment out or remove the block marked `--- STUBBED RESPONSE FOR TESTING ---`.
        *   Uncomment the block marked `--- ACTUAL MEM0 CALL ---`.

2.  **Configure Mem0 Instance:**
    *   At the beginning of `app.py`, the `mem0_instance` is initialized. By default (if the stubbed configuration part is also bypassed or modified), it will try to use OpenAI for LLM and Embeddings, and Chroma for the Vector Store.
    *   **Environment Variables:** For live OpenAI operations, ensure the `OPENAI_API_KEY` environment variable is set with your valid key:
        ```bash
        export OPENAI_API_KEY='your_actual_openai_api_key'
        ```
    *   **Custom Mem0 Configuration:** If you wish to use other LLMs, embedders, or vector stores supported by Mem0, you'll need to modify the `mem0_instance` initialization in `app.py` according to the [Mem0 documentation](https://docs.mem0.ai/). The file currently contains a commented-out example of how `mem0_instance` was configured for testing with dummy OpenAI keys, which can be adapted.

## Basic Usage (Web UI)

1.  **Open the Application:** Once the Flask server is running (e.g., on `http://127.0.0.1:8087/`), open this URL in your web browser.

2.  **Enter User ID:** All memories are associated with a `User ID`. Enter a unique identifier for the user whose memories you want to manage.

3.  **Operations:**
    *   **Add Memory:**
        *   Enter the message or context to remember in the "Message/Context to Remember" text area.
        *   Click "Add Memory". The API response will be displayed.
    *   **Search Memories:**
        *   Enter your search query in the "Search Query" field.
        *   Click "Search Memories". Results will appear in the API response area.
    *   **Get All Memories:**
        *   Ensure the User ID field is filled.
        *   Click "Get All Memories". All memories for that user will be displayed.
    *   **Delete Memory:**
        *   Enter the `Memory ID` of the memory you wish to delete (you can find this ID from the "Get All Memories" or "Search Memories" response).
        *   Ensure the User ID field is also correctly set for the user who owns that memory.
        *   Click "Delete Memory".

4.  **API Response:** The raw JSON response from the backend API will be shown in the "API Response" text area for each operation.

## Deactivating the Virtual Environment
When you are finished, you can deactivate the virtual environment:
```bash
deactivate
```
This command works if you are in the directory where you activated the environment or if your shell remembers the context.
