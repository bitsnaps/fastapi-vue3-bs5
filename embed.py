# requires:
# pip install torch #==2.4.1
# pip install transformers #==4.45.0
# pip install einops #==0.8.0
import torch
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer

load_dotenv()

# Load the pre-trained model and tokenizer
model_id = 'nomic-ai/nomic-embed-text-v1.5'
model = AutoModel.from_pretrained(model_id, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)


# Text to be processed
text = "Your input text here"

# Tokenize the text and convert to tensor
inputs = tokenizer(text, return_tensors="pt")

# Get the embeddings
with torch.no_grad():
    embeddings = model(**inputs).last_hidden_state[:, 0, :]

import numpy as np

print(np.shape(embeddings))
# output: torch.Size([1, 768])

# Much simpler but depends on:
# pip install sentence-transformers==3.1.1
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_id, trust_remote_code=True)
sentences = ['search_document: TSNE is a dimensionality reduction algorithm created by Laurens van Der Maaten']
embeddings = model.encode(sentences)

print(np.shape(embeddings))
# outputs: (1, 768)

