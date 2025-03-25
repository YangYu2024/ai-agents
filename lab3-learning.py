import os
from autogen import AssistantAgent, UserProxyAgent

# Setup Ollama configuration
ollama_config = {
    "config_list": [
        {
            "model": "llama3.2",
            "api_type": "ollama",
            "client_host": "http://localhost:11434",  # Adjust based on your Ollama setup
            "stream": False,
            "temperature": 0,  # Adjust temperature as needed
        }
    ]
}

# Create the AssistantAgent
assistant = AssistantAgent(
    name="LearningAgent",
    llm_config=ollama_config,
    system_message="I am a learning agent. Provide feedback to improve my recommendations.",
)

# Create the UserProxyAgent for user interaction
user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"executor": None},  # No code execution needed
)

# Define a simple machine learning model to analyze user feedback
# For simplicity, this example uses a basic pattern recognition approach.
# In practice, you would use a more sophisticated ML model.

def analyze_feedback(feedback):
    # Example: Count positive/negative feedback
    positive_count = feedback.count("good")
    negative_count = feedback.count("bad")
    return positive_count, negative_count

# Define a function to refine recommendations based on feedback
def refine_recommendations(feedback):
    positive_count, negative_count = analyze_feedback(feedback)
    if positive_count > negative_count:
        return "Recommend more similar products."
    else:
        return "Suggest alternative products."

# Run the agent in a loop to continuously learn and adapt
while True:
    # Initiate chat with the user
    chat_result = user_proxy.initiate_chat(assistant, message="Recommend a product.")
    
    # Get user feedback
    user_feedback = input("Please provide feedback on the recommendation: ")
    
    # Refine recommendations based on feedback
    refined_recommendation = refine_recommendations(user_feedback)
    
    # Update the agent's knowledge with the refined recommendation
    assistant.system_message += f"\nLearned: {refined_recommendation}"
    
    # Continue the loop until termination
    if "exit" in user_feedback.lower():
        break
