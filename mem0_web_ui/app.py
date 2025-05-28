from flask import Flask, request, jsonify, render_template
from mem0 import Memory

app = Flask(__name__)

# Initialize Mem0
# This will use the default configuration for Mem0,
# which by default might try to use OpenAI and require OPENAI_API_KEY
# For now, we are not handling the API key explicitly in the app initialization.
from mem0.configs.base import MemoryConfig
from mem0.llms.configs import LlmConfig # Concrete class
from mem0.embeddings.configs import EmbedderConfig # Concrete class

# The goal is to initialize Mem0 so the Flask app can run, even if LLM/embedding ops fail.
# We use the concrete LlmConfig and EmbedderConfig with "openai" provider and dummy keys.
# This should satisfy MemoryConfig's type expectations.

print("--- Mem0 Web UI: Initializing Mem0 with Dummy API Keys for Local Testing ---")
MEM0_INITIALIZED_SUCCESSFULLY = False
FALLBACK_TO_DEFAULT_MEM0_INIT = False
try:
    print("Configuring LLM (OpenAI provider) with a dummy API key...")
    llm_provider_config = LlmConfig(
        provider="openai", # Explicitly use "openai" provider
        config={
            "api_key": "DUMMY_LLM_API_KEY_FOR_TESTING",
            "model": "gpt-3.5-turbo" 
        }
    )
    print("LLM configuration prepared.")

    print("Configuring Embedder (OpenAI provider) with a dummy API key...")
    embedder_provider_config = EmbedderConfig(
        provider="openai", # Explicitly use "openai" provider
        config={
            "api_key": "DUMMY_EMBEDDER_API_KEY_FOR_TESTING",
            "model": "text-embedding-ada-002"
        }
    )
    print("Embedder configuration prepared.")

    print("Creating MemoryConfig...")
    # Vector store will use its default (Chroma, in-memory compatible).
    memory_config_for_testing = MemoryConfig(
        llm=llm_provider_config,
        embedder=embedder_provider_config
        # Not specifying vector_store, so it uses default (Chroma)
    )
    print("MemoryConfig created.")

    print("Initializing mem0.Memory with the test configuration...")
    mem0_instance = Memory(config=memory_config_for_testing)
    print("SUCCESS: mem0.Memory initialized using MemoryConfig with dummy API keys for OpenAI provider.")
    MEM0_INITIALIZED_SUCCESSFULLY = True

except ImportError as e:
    print(f"ERROR: ImportError during Mem0 custom initialization: {e}")
    FALLBACK_TO_DEFAULT_MEM0_INIT = True
except Exception as e:
    print(f"ERROR: Exception during Mem0 custom initialization: {e}")
    print(f"Type of exception: {type(e)}")
    FALLBACK_TO_DEFAULT_MEM0_INIT = True

if FALLBACK_TO_DEFAULT_MEM0_INIT:
    print("Falling back to default mem0.Memory() initialization due to errors.")
    # This will require OPENAI_API_KEY in env or will fail if unset.
    mem0_instance = Memory() 

if not MEM0_INITIALIZED_SUCCESSFULLY and not FALLBACK_TO_DEFAULT_MEM0_INIT:
    print("CRITICAL ERROR: Mem0 instance may not be properly initialized and no fallback occurred.")

if not MEM0_INITIALIZED_SUCCESSFULLY:
    print("WARNING: Mem0 was NOT initialized with the desired local/mock configuration (dummy keys). It may be using defaults or failed initialization if fallback also failed.")
print("--- Mem0 Initialization End ---")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/memory/add', methods=['POST'])
def add_memory():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON payload."}), 400

    user_id = data.get('user_id')
    text_to_remember = data.get('data')

    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required."}), 400
    if not text_to_remember:
        return jsonify({"status": "error", "message": "data to remember is required."}), 400

    # --- STUBBED RESPONSE FOR TESTING ---
    print(f"STUB: Add memory for user_id: {user_id}, data: {text_to_remember}")
    return jsonify({
        "status": "success", 
        "message": "Memory added (stubbed)", 
        "user_id": user_id, 
        "data_received": text_to_remember
    }), 200
    # --- END STUBBED RESPONSE ---

    # --- ACTUAL MEM0 CALL (Commented out for stubbed testing) ---
    # try:
    #     messages = [{"role": "user", "content": text_to_remember}]
    #     mem0_instance.add(messages=messages, user_id=user_id)
    #     return jsonify({"status": "success", "message": "Memory added successfully."}), 200
    # except KeyError as e:
    #     print(f"Error adding memory: Missing key {e}")
    #     return jsonify({"status": "error", "message": f"Missing expected data: {e}"}), 400
    # except Exception as e:
    #     print(f"Error adding memory: {e}")
    #     return jsonify({"status": "error", "message": f"Failed to add memory. Server error: {str(e)}"}), 500
    # --- END ACTUAL MEM0 CALL ---


@app.route('/api/memory/search', methods=['GET'])
def search_memory():
    user_id = request.args.get('user_id')
    query = request.args.get('query')

    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required."}), 400
    if not query:
        return jsonify({"status": "error", "message": "query is required."}), 400

    # --- STUBBED RESPONSE FOR TESTING ---
    print(f"STUB: Search memory for user_id: {user_id}, query: {query}")
    stubbed_results = [
        {"id": "stub_search_123", "memory": f"Stubbed search result 1 for '{query}' in user {user_id}", "user_id": user_id, "created_at": "2024-01-01T10:00:00Z", "metadata": {"source": "stub"}},
        {"id": "stub_search_456", "memory": f"Stubbed search result 2 for '{query}' in user {user_id}", "user_id": user_id, "created_at": "2024-01-01T10:05:00Z", "metadata": {"source": "stub"}}
    ]
    return jsonify({"status": "success", "results": stubbed_results, "message": "Search successful (stubbed)"}), 200
    # --- END STUBBED RESPONSE ---

    # --- ACTUAL MEM0 CALL (Commented out for stubbed testing) ---
    # try:
    #     results = mem0_instance.search(user_id=user_id, query=query)
    #     if not results: # Assuming results can be an empty list or None if no memories found
    #         return jsonify({"status": "success", "results": [], "message": "No memories found matching your query."}), 200
    #     # Ensure 'results' key exists; structure might vary (e.g. results.get("results", []))
    #     return jsonify({"status": "success", "results": results if isinstance(results, list) else results.get("results", [])}), 200
    # except Exception as e:
    #     print(f"Error searching memory: {e}")
    #     return jsonify({"status": "error", "message": f"Failed to search memory. Server error: {str(e)}"}), 500
    # --- END ACTUAL MEM0 CALL ---


@app.route('/api/memory/get_all', methods=['GET'])
def get_all_memories():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required."}), 400

    # --- STUBBED RESPONSE FOR TESTING ---
    print(f"STUB: Get all memories for user_id: {user_id}")
    stubbed_memories = [
        {"id": "stub_mem_abc", "memory": "This is stubbed memory Alpha for user.", "user_id": user_id, "created_at": "2024-01-01T12:00:00Z", "metadata": {"type": "reminder"}},
        {"id": "stub_mem_def", "memory": "This is stubbed memory Beta for user.", "user_id": user_id, "created_at": "2024-01-01T12:05:00Z", "metadata": {"type": "note"}},
        {"id": "stub_mem_ghi", "memory": "This is stubbed memory Gamma for user.", "user_id": user_id, "created_at": "2024-01-01T12:10:00Z", "metadata": {"type": "event"}}
    ]
    return jsonify({"status": "success", "memories": stubbed_memories, "message": "All memories retrieved (stubbed)"}), 200
    # --- END STUBBED RESPONSE ---

    # --- ACTUAL MEM0 CALL (Commented out for stubbed testing) ---
    # try:
    #     memories = mem0_instance.get_all(user_id=user_id)
    #     if not memories: # Assuming memories can be an empty list or None
    #         return jsonify({"status": "success", "memories": [], "message": "No memories found for this user."}), 200
    #     return jsonify({"status": "success", "memories": memories}), 200
    # except Exception as e:
    #     print(f"Error retrieving all memories: {e}")
    #     return jsonify({"status": "error", "message": f"Failed to retrieve all memories. Server error: {str(e)}"}), 500
    # --- END ACTUAL MEM0 CALL ---


@app.route('/api/memory/delete', methods=['DELETE'])
def delete_memory_endpoint():
    user_id = request.args.get('user_id')
    memory_id = request.args.get('memory_id')

    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required."}), 400
    if not memory_id:
        return jsonify({"status": "error", "message": "memory_id is required."}), 400
        
    # --- STUBBED RESPONSE FOR TESTING ---
    print(f"STUB: Delete memory for user_id: {user_id}, memory_id: {memory_id}")
    return jsonify({"status": "success", "message": f"Memory {memory_id} deleted (stubbed)"}), 200
    # --- END STUBBED RESPONSE ---

    # --- ACTUAL MEM0 CALL (Commented out for stubbed testing) ---
    # try:
    #     # It might be good to check if memory_id exists before attempting deletion,
    #     # but Mem0 library might handle non-existent IDs gracefully.
    #     # For now, directly calling delete.
    #     mem0_instance.delete(user_id=user_id, memory_id=memory_id)
    #     return jsonify({"status": "success", "message": f"Memory {memory_id} deleted successfully."}), 200
    # except Exception as e:
    #     print(f"Error deleting memory: {e}")
    #     return jsonify({"status": "error", "message": f"Failed to delete memory. Server error: {str(e)}"}), 500
    # --- END ACTUAL MEM0 CALL ---

if __name__ == '__main__':
    app.run(debug=True)
