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
    embedding_df =df.drop(columns=["text"])  # all numeric columns
    print("Loaded existing embeddings from CSV", '\n')
else:


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

from openai import OpenAI
client = OpenAI(api_key="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")


def createPrompt(new_query):
    user_embedding = model.encode([new_query])  # Create an embedding for the user query
    # Step 3: Calculate similarity
    similarities = cosine_similarity(user_embedding, embedding_df.values)

    # Step 4: Find the index of the most similar embedding
    ####most_similar_index = similarities.argmax()
    most_similar_index = similarities[0].argsort()[-20:][::-1]
    best_answer = [text_data[i] for i in most_similar_index]

    # Retrieve the corresponding text
    #most_similar_text = text_data[most_similar_index]
    most_similar_text = "\n\n".join(best_answer)
    prompt = most_similar_text
    return prompt

n = 0

# Remove bad words
blockprompt = "Block the response/text completely from this list [porn, nude, xxx, explicit, hentai, strip, erotic, hardcore, fetish, sex, blowjob, orgy, intercourse,kill, murder, suicide, abuse, torture, beheading, execution, bomb,drugs, cocaine, heroin, marijuana,fuck, slut, bastard, asshole, cunt, dick, pussy, mf, wtf, damn]"

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system",
               "content": "You are a conversational AI as Tutor teaching from book Chemistry2e-OpenStax.pdf that suggests relevant next questions to keep the discussion engaging."},
              {"role": "system", "content": blockprompt},
              {"role": "user", "content": "Start teaching me Chemistry from a book Chemistry2e-OpenStax.pdf"}],
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
        #messages=[{"role": "system", "content": "You are a conversational AI as Tutor for Chemistry that suggests relevant next questions to keep the discussion engaging."},
        messages=[
            {"role": "system", "content": "You must ONLY use the context provided and it is from a book Chemistry2e-OpenStax.pdf"},
            {"role": "system", "content": blockprompt},
            {"role": "system", "content": f"Context:\n{prompt}"},
            {"role": "user", "content": new_query}
        ],
        temperature=0,
        stream=False,
    )
    # Generate follow-up questions
    answer = stream.choices[0].message.content
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Tutor teaching from a book Chemistry2e-OpenStax.pdf"},
            {"role": "system", "content": "Suggest two engaging follow-up questions based on the previous response and it should be from the context provided."},
            {"role": "system", "content": blockprompt},
            {"role": "user", "content": answer}
        ],
        temperature=0,
        stream=False
    )
    print("S&S ChemGenius: ")
    print(answer, '\n')
    print("Suggested Questions: ")
    print(stream.choices[0].message.content)

    if ( n > 25):
        break



print("Thanks for using this Tutor program, bye")
