import tkinter as tk
from tkinter import scrolledtext, END
from openai import OpenAI

import pymupdf as fitz
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the PDF file and extract text

pdf_file_path = r"C:\Shaunak\AI Tutor\Chemistry2e-OpenStax.pdf"
text_data = []

if os.path.exists("embeddingsChem.csv"):
    df = pd.read_csv("embeddingsChem.csv",encoding='utf-8')
    # Separate columns
    text_data = df["text"].tolist()
    #print(df.columns)
    embedding_df =df.drop(columns=["text"])  # all numeric columns
    print("Loaded existing embeddings from CSV", '\n')
else:


    #with fitz.open(pdf_file_path) as pdf:
    #    for page in pdf:
    #        text_data.append(page.get_text())
    with fitz.open(pdf_file_path) as pdf:
        for i, page in enumerate(pdf, start=1):  # start=1 to make it human-readable
            page_text = page.get_text()
            tagged_text = f"[Page {i}]\n{page_text}"
            text_data.append(tagged_text)

    # Step 2: Preprocess the text
    text_data = [line.strip() for line in text_data if line.strip()]

    # Step 3: Generate embeddings
    #model = SentenceTransformer('all-MiniLM-L6-v2')  # or any other suitable model
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings = model.encode(text_data)

    # Step 4: Store the embeddings
    df = pd.DataFrame(embeddings)
    df.insert(0, "text", text_data)  # first column is the text
    df.to_csv('embeddingsChem.csv', index=False,encoding="utf-8")
    embedding_df = df.drop(columns=["text"])  # all numeric columns
    print("Generated and saved new embeddings")

#model = SentenceTransformer('all-MiniLM-L6-v2')  # Use the same model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def createPrompt(new_query):
    user_embedding = model.encode([new_query])  # Create an embedding for the user query
    # Step 3: Calculate similarity
    similarities = cosine_similarity(user_embedding, embedding_df.values)

    # Step 4: Find the index of the most similar embedding
    ####most_similar_index = similarities.argmax()
    most_similar_index = similarities[0].argsort()[-20:][::-1]
    best_answer = [text_data[i] for i in most_similar_index]
#    blockprompt = "\n\n".join(top_chunks)

    ####best_answer = text_data[most_similar_index]
    #print("ANS FROM TEXT: ", best_answer, "\n")
    # Retrieve the corresponding text
    #most_similar_text = text_data[most_similar_index]
    most_similar_text = "\n\n".join(best_answer)
    #print("Similar query text from book: ", most_similar_text, "\n")
    prompt = most_similar_text
    return prompt

client = OpenAI(api_key="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")
#You can generate a key by signing into platform.openai.com

blockprompt = "Block the response/text completely from this list [porn, nude, xxx, explicit, hentai, strip, erotic, hardcore, fetish, sex, blowjob, orgy, intercourse,kill, murder, suicide, abuse, torture, beheading, execution, bomb,drugs, cocaine, heroin, marijuana,fuck, slut, bastard, asshole, cunt, dick, pussy, mf, wtf, damn]"

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system",
               "content": "You are a conversational AI as Tutor teaching from book Chemistry2e-OpenStax.pdf that suggests relevant next questions to keep the discussion engaging."},
              {"role": "system", "content": blockprompt},
              {"role": "user", "content": "Start teaching me Chemistry from a book Chemistry2e-OpenStax.pdf"}],
    stream=False,

)
# Function to send the user input to ChatGPT and display the response
def get_chatgpt_response():
    user_query = user_input.get("1.0", tk.END).strip()  # Get user input
    if not user_query:
        response_display.insert(tk.END, "Please enter a query.\n")
        return

    try:
        # Call the OpenAI API
        prompt = createPrompt(user_query)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # messages=[{"role": "system", "content": "You are a conversational AI as Tutor for Chemistry that suggests relevant next questions to keep the discussion engaging."},
            messages=[
                {"role": "system",
                 "content": "You must ONLY use the context provided and it is from a book Chemistry2e-OpenStax.pdf"},
                #        {"role": "system",  "content": "You must ONLY use the context provided"},
                #        {"role": "system", "content": "Suggest two engaging follow-up questions based on the previous response and it should be from the context provided."},
                {"role": "system", "content": blockprompt},
                {"role": "system", "content": f"Context:\n{prompt}"},
                {"role": "user", "content": user_query}
            ],
            temperature=0,
            stream=False,
        )
        # Generate follow-up questions
        answer = stream.choices[0].message.content

        # Display the response in the text area
        response_display.insert(tk.END, f"You: {user_query}\n")
        response_display.insert(tk.END, f"S&S Tutor: {answer}\n\n")
        # Scroll to the bottom
        response_display.see(END)
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

# Bind Enter key
window.bind('<Return>', lambda event: get_chatgpt_response())

# Send button
send_button = tk.Button(window, text="Send", command=get_chatgpt_response)
send_button.pack(pady=5)

# Response display area
response_label = tk.Label(window, text="S&S Tutor Response:")
response_label.pack(pady=5)

response_display = scrolledtext.ScrolledText(window, height=20, width=70, wrap=tk.WORD)
response_display.pack(pady=5)

# Run the application
window.mainloop()
