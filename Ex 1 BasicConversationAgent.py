"""
Simple Chat Agent using OpenAI API
A basic conversational AI that maintains chat history

"""
from openai import OpenAI
import os 
from dotenv import load_dotenv

 
# Initialize the OpenAI client
# Option 1: API key from environment variable (recommended)
# Option 2: Pass it directly: client = OpenAI(api_key="your-api-key-here")

env_path = os.path.join(r'C:/Users/biswa/OneDrive/Documents/Agentic ERA/Variables.env')

load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
def chat_agent():

    """Main chat function that handles the conversation loop"""
    # Store conversation history
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Chat Agent Started! (Type 'quit' to exit)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        # Exit condition
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break       

        if not user_input:
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # or "gpt-4o" for better responses
                messages=messages,
                temperature=0.7,
                max_tokens=500

            )

            # Get assistant's reply
            assistant_message = response.choices[0].message.content
            # Add assistant's reply to history
            messages.append({"role": "assistant", "content": assistant_message})           
            # Display the response
            print(f"\nAssistant: {assistant_message}")

        except Exception as e:

            print(f"\nError: {e}")

            print("Please check your API key and internet connection.") 

if __name__ == "__main__":

    chat_agent()