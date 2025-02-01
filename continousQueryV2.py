import pymupdf as fitz
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the PDF file and extract text
#pdf_file_path = r"C<location>"
pdf_file_path = r"C:\temp\Chemistry2e-OpenStax.pdf"
text_data = []

# Extract text from each page
with fitz.open(pdf_file_path) as pdf:
    for page in pdf:
        text_data.append(page.get_text())

# Step 2: Preprocess the text
text_data = [line.strip() for line in text_data if line.strip()]

# Step 3: Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')  # or any other suitable model
embeddings = model.encode(text_data)

# Step 4: Store the embeddings
embedding_df = pd.DataFrame(embeddings)
embedding_df.to_csv('embeddingsChem.csv', index=False)



# Step 1: Load the embeddings from CSV
#embedding_df = pd.read_csv('embeddings.csv')

# Assuming you have a separate file with the original text data
#text_data = pd.read_csv('embeddingsChem.csv', header=None).iloc[:, 0].tolist()

# Step 2: Initialize the model and generate embedding for the user query
model = SentenceTransformer('all-MiniLM-L6-v2')  # Use the same model

from openai import OpenAI
client = OpenAI(api_key="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")

def createPrompt(new_query):
    user_embedding = model.encode([new_query])  # Create an embedding for the user query
    # Step 3: Calculate similarity
    similarities = cosine_similarity(user_embedding, embedding_df.values)

    # Step 4: Find the index of the most similar embedding
    most_similar_index = similarities.argmax()

    # Retrieve the corresponding text
    most_similar_text = text_data[most_similar_index]
    prompt = f"Context: {most_similar_text}\nUser Query: {new_query}\nResponse:"
    return prompt

n = 0

# Remove bad words
blockprompt = "Block the response/text completely from this list [porn, nude, xxx, explicit, hentai, strip, erotic, hardcore, fetish, sex, blowjob, orgy, intercourse,kill, murder, suicide, abuse, torture, beheading, execution, bomb,drugs, cocaine, heroin, marijuana,fuck, slut, bastard, asshole, cunt, dick, pussy, mf, wtf, damn]"

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You are a conversational AI as Tutor for Chemistry that suggests relevant next questions to keep the discussion engaging."},
              {"role": "system", "content": blockprompt},
              {"role": "user", "content": "Start teaching me Chemistry"}],
    stream=False,
)

while True:
    n = n +1
    line = input(">>Enter your questions here, write exit or just enter to quit the program: ")
    if line == "" or line == "exit":
        break
    else:
        new_query = line

    prompt = createPrompt(new_query)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a conversational AI as Tutor for Chemistry that suggests relevant next questions to keep the discussion engaging."},
                  {"role": "system", "content": blockprompt},
                  {"role": "user", "content": prompt}],
        stream=False,
    )
    # Generate follow-up questions
    answer = stream.choices[0].message.content
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Suggest two engaging follow-up questions based on the previous response."},
            {"role": "user", "content": answer}
        ],
        stream=False
    )
    print("S&S ChemGenius: ")
    print(answer)
    print("Suggested Questions: ")
    print(stream.choices[0].message.content)
#    Set limit here to safguard against using up too many credits from an API
#    delete the two lines below for no limt

    if ( n > 25):
        break



print("Thanks for using this Tutor program, bye")

