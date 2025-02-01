import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI

client = OpenAI(api_key="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")
#You can generate a key by signing into platform.openai.com

# Function to send the user input to ChatGPT and display the response
def get_chatgpt_response():
    user_query = user_input.get("1.0", tk.END).strip()  # Get user input
    if not user_query:
        response_display.insert(tk.END, "Please enter a query.\n")
        return

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            #    model="gpt-4o-mini",
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_query}],
            stream=False,
        )
        # Get the text of the response
        chatgpt_response = response.choices[0].message.content
        # Display the response in the text area
        response_display.insert(tk.END, f"You: {user_query}\n")
        response_display.insert(tk.END, f"S&S Tutor: {chatgpt_response}\n\n")
    except Exception as e:
        response_display.insert(tk.END, f"Error: {str(e)}\n")

    # Clear the user input area
    user_input.delete("1.0", tk.END)

# Create the main UI window
window = tk.Tk()
window.title("Shaun & Sparsh Tutor")
window.geometry("600x600")

# Input area
input_label = tk.Label(window, text="Enter your query:")
input_label.pack(pady=5)

user_input = tk.Text(window, height=5, width=70)
user_input.pack(pady=5)

# Send button
send_button = tk.Button(window, text="Send", command=get_chatgpt_response)
send_button.pack(pady=5)

# Response display area
response_label = tk.Label(window, text="ChatGPT Response:")
response_label.pack(pady=5)

response_display = scrolledtext.ScrolledText(window, height=20, width=70, wrap=tk.WORD)
response_display.pack(pady=5)

# Run the application
window.mainloop()