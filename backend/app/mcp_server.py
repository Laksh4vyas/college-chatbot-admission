from mcp.server.fastmcp import FastMCP
from app.services.chatbot import process_chat

# Create an MCP server
mcp = FastMCP("College Admission Chatbot MCP")

@mcp.tool()
def ask_admission_query(message: str) -> str:
    """
    Ask the college admission chatbot a query.
    This tool uses a soft-voting ensemble of machine learning models to answer intent-based questions
    like admissions, housing, scholarships, and deadlines.
    
    Args:
        message: The user's query about college admission.
    """
    result = process_chat(message)
    return f"Answer: {result['answer']} (Confidence: {result['confidence']:.2f}, Model: {result['model']})"

# To run the MCP server, you would typically run this file via standard CLI or use FastMCP's built-in run method
# Example: mcp run backend/app/mcp_server.py:mcp
if __name__ == "__main__":
    mcp.run()
