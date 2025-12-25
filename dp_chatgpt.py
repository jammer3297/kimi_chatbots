import openai
import os

# Set up your OpenAI API key (recommended to use environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    openai.api_key = input("Enter your OpenAI API key: ").strip()

def chat_with_gpt():
    # Initialize conversation history with system message
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Respond concisely."}
    ]

    print("ChatGPT CLI - Type 'exit' to quit")
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue

            # Exit condition
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            # Add user message to history
            messages.append({"role": "user", "content": user_input})

            # Get API response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )

            # Extract and display response
            assistant_response = response.choices[0].message.content
            print(f"\nAssistant: {assistant_response}")

            # Add assistant response to history
            messages.append({"role": "assistant", "content": assistant_response})

        except openai.error.AuthenticationError:
            print("Error: Invalid API key. Please check your OpenAI API key.")
            break
        except openai.error.APIError as e:
            print(f"API Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    chat_with_gpt()