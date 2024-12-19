# Groq Function Chat + SQLite DB Support (w/ Llama3 LLM)

## Overview
Groq Function Chat is a Python-based console application that uses the Groq API to perform arithmetic operations such as addition, subtraction, multiplication, and division. It demonstrates how to leverage Groq's function-calling capabilities in a conversational environment. Groq API uses LLama 3 for the prompts and functions.

---

## Features
- Perform basic arithmetic operations: addition, subtraction, multiplication, and division.
- Interact via a console chat interface.
- Dynamically call functions using the Groq API.
- Load API keys securely from a `.env` file using `python-dotenv`.

---

## Requirements
- Python 3.7+
- `requests` library
- `python-dotenv` library
- `sqlite db browser` https://sqlitebrowser.org/dl/

---

## Setup Instructions

### 1. Clone the Repository
```bash
# Clone this repository to your local machine
git clone https://github.com/your-repository/groq-function-chat.git
cd groq-function-chat
```

### 2. Install Dependencies
```bash
# Install required Python libraries
pip install requests python-dotenv
```

### 3. Set Up the Environment Variables
Create a `.env` file in the project directory and add your Groq API key & Database Information:
```env
API_KEY=your_actual_api_key_here
```
Replace `your_actual_api_key_here` with your actual Groq API key.

DATABASE_URL=sqlite:///results.db  # Optional: Change if using a different DB


---

## Running the Application
Run the script to start the console chat application:
```bash
python main.py
```

### Example Usage
```plaintext
Welcome to the Groq Function Chat!
You can ask the system to perform addition, subtraction, multiplication, or division.

You: Add 5 and 10
Result: 15

You: Divide 20 by 4
Result: 5.0

You: Quit
Goodbye!
```

---

## File Structure
```
.
├── groq_function_chat.py   # Main application script
├── .env                   # Environment variables file
├── requirements.txt       # Dependencies (optional)
```

---

## Key Components

### 1. Arithmetic Functions
- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)`

### 2. Groq API Integration
The `call_groq_function` function interacts with the Groq API to parse user input and call the appropriate function.

### 3. Console Interface
The console_chat function handles the interactive user experience and stores results in the database after each calculation.

### 4. Database Integration
The CalculationResult model is used to store results of operations in an SQLite database.
The database is configured through the DATABASE_URL environment variable.


---

## Notes
- Ensure that the 'env' has your GROQ API key in it.
- The application gracefully handles division by zero with an error message.
- This project demonstrates how to integrate Groq's advanced API features into a Python application.

---

## Acknowledgements
- [Groq API Documentation](https://api.groq.com)
- [Requests Library Documentation](https://docs.python-requests.org/)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [SQLite Browser Documentation]([https://pypi.org/project/python-dotenv/](https://github.com/sqlitebrowser/sqlitebrowser/wiki))

---

