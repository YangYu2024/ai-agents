import json
import os
from crewai import Crew, Task, Agent
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "testapikey"

# Use a lightweight LLM model optimized for CPU
ollama_llm = ChatOpenAI(
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434"
)

# Simulated function to book a flight
def book_flight(flight_number: str):
    print(f"Booking flight {flight_number}...")
    return json.dumps({"status": "confirmed", "flight_number": flight_number})

# Define the AI agents
booking_agent = Agent(
    role="Airline Booking Assistant",
    goal="Help users find and book flights efficiently.",
    backstory="You are an expert airline booking assistant, providing the best travel options with clear information.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for planning tasks
planning_agent = Agent(
    role="Planning Assistant",
    goal="Assist in planning and organizing travel details.",
    backstory="You are skilled at planning and organizing travel itineraries efficiently.",
    verbose=True,
    llm=ollama_llm,
)

# Define the tasks with expected outputs
# Create a task to extract travel details (source, destination, date) using the LLM.
extract_travel_info_task = Task(
    description=(
        "Extract destination and date from {user_request}"
    ),
    agent=booking_agent,
    expected_output="A JSON object containing 'destination', and 'date'."
)

# Use the planning agent for finding flights
find_flights_task = Task(
    description="Find available flights for the extracted destination and date.",
    agent=planning_agent,  # Use the planning agent here
    expected_output="A JSON list of available flights, including flight number, airline, departure time, and price."
)

present_flights_task = Task(
    description="Present flight options in a user-friendly format and ask the user to choose one. The list of flight should not be in JSON format and should have a number by each choice.",
    agent=booking_agent,
    expected_output="The selected flight number chosen by the user. If no response, just use 1."
)