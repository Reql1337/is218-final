import requests
import json
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# API Endpoint and API Key
API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("API_KEY")  # Ensure your .env file contains API_KEY

# SQLAlchemy setup
Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///results.db")  # Default to SQLite if DATABASE_URL is not set

# Define the Result model to store the calculation results
class CalculationResult(Base):
    __tablename__ = 'calculation_results'

    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False)
    operand_a = Column(Float, nullable=False)
    operand_b = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Set up the database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)  # Create the tables if they don't exist

# Define functions for arithmetic operations
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero"

# Function to call the Groq API
def call_groq_function(prompt, functions, model="llama3-8b-8192"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "functions": functions,
        "function_call": "auto",
    }

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Check if the model called a function
        if "function_call" in data["choices"][0]["message"]:
            function_name = data["choices"][0]["message"]["function_call"]["name"]
            arguments = json.loads(data["choices"][0]["message"]["function_call"]["arguments"])
            return function_name, arguments

        return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

# Function to store calculation results in the database
def store_calculation_result(operation, a, b, result):
    session = Session()
    calc_result = CalculationResult(
        operation=operation,
        operand_a=a,
        operand_b=b,
        result=result
    )
    session.add(calc_result)
    session.commit()
    session.close()

# Main console application
def console_chat():
    print("Welcome to the Groq Function Chat!")
    print("You can ask the system to perform addition, subtraction, multiplication, or division.")

    functions = [
        {
            "name": "add",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number."},
                    "b": {"type": "number", "description": "The second number."}
                },
                "required": ["a", "b"]
            },
        },
        {
            "name": "subtract",
            "description": "Subtract two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number."},
                    "b": {"type": "number", "description": "The second number."}
                },
                "required": ["a", "b"]
            },
        },
        {
            "name": "multiply",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number."},
                    "b": {"type": "number", "description": "The second number."}
                },
                "required": ["a", "b"]
            },
        },
        {
            "name": "divide",
            "description": "Divide two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number."},
                    "b": {"type": "number", "description": "The second number."}
                },
                "required": ["a", "b"]
            },
        }
    ]

    while True:
        prompt = input("You: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        function_name, arguments = call_groq_function(prompt, functions)

        if function_name and arguments:
            if function_name == "add":
                result = add(arguments["a"], arguments["b"])
            elif function_name == "subtract":
                result = subtract(arguments["a"], arguments["b"])
            elif function_name == "multiply":
                result = multiply(arguments["a"], arguments["b"])
            elif function_name == "divide":
                result = divide(arguments["a"], arguments["b"])
            else:
                result = "Error: Unknown function called"

            print(f"Result: {result}")
            
            # Store the result in the database
            store_calculation_result(function_name, arguments["a"], arguments["b"], result)
        else:
            print("No function call was made or an error occurred.")

if __name__ == "__main__":
    console_chat()
