# install pandas pyMuPdf sentence-transformers sklearn
# This program
# Reads pdf file (breaks down into smaller components such as words, subwords, or characters)
# and Generate Embeddings (model captures contextual and semantic relationships between the words)
# It stores the result (dense numerical vector (embedding) for each input text) into a file
# We are giving a query as an input and it finds a vector from the embedding(above files)
# and returns all similarities associated with the query from the pdf file.

import pymupdf as fitz
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the PDF file and extract text
#pdf_file_path = r"C:\Shaunak\AI Tutor\PaperForREf.pdf"
pdf_file_path = r"C:\Shaunak\AI Tutor\Chemistry2e-OpenStax.pdf"
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

print("Check if embeddingsChem.csv is generated and it has some content - Mainly numbers in cells")

user_query = "What are different states of a Matter and give me their examples"  # Replace with the actual user query
user_embedding = model.encode([user_query])  # Create an embedding for the user query

# Step 3: Calculate similarity
similarities = cosine_similarity(user_embedding, embedding_df.values)

# Step 4: Find the index of the most similar embedding
most_similar_index = similarities.argmax()

print("Index from the embedding - does not make sense: ", most_similar_index, '\n \n')
# Retrieve the corresponding text
most_similar_text = text_data[most_similar_index]

print(f"Most relevant text: {most_similar_text}")
