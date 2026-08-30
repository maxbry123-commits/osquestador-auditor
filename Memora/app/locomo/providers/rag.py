# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import os
import time
from collections import defaultdict

import numpy as np
import tiktoken
from dotenv import load_dotenv
from jinja2 import Template
from omegaconf import DictConfig
from tqdm import tqdm

from utils import load_data
from memora.utils.llm import get_aoai_chat_completion_client
from memora.utils.embedding import get_aoai_embedding_client

load_dotenv()

# Using the same prompt template as Mem0/Memora for fair comparison
PROMPT = """
    You are an intelligent memory assistant that answers questions based on retrieved context.

    # CONTEXT:
    You have access to retrieved context from a conversation between two speakers. This context contains timestamped information that may be relevant to answering the question.

    # INSTRUCTIONS:
    1. Carefully analyze the provided context
    2. Pay special attention to the timestamps to determine the answer
    3. If the question asks about a specific event or fact, look for direct evidence in the context
    4. If the context contains contradictory information, prioritize the most recent information in terms of timestamp
    5. If there is a question about time references (like "last year", "two months ago", etc.), calculate the actual date based on the context timestamp. For example, if context from 4 May 2022 mentions "went to India last year," then the trip occurred in 2021.
    6. Always convert relative time references to specific dates, months, or years. For example, convert "last year" to "2022" or "two months ago" to "March 2023" based on the context timestamp. Ignore the reference while answering the question.
    7. Focus only on the content of the context. Do not confuse character names mentioned in context with the actual speakers.
    8. The answer should be less than 5-6 words.


    # APPROACH (Think step by step):
    1. First, examine all parts of the context that contain information related to the question
    2. Examine the timestamps and content carefully
    3. Look for explicit mentions of dates, times, locations, or events that answer the question
    4. If the answer requires calculation (e.g., converting relative time references), show your work
    5. Formulate a precise, concise answer based solely on the evidence in the context
    6. Double-check that your answer directly addresses the question asked
    7. Ensure your final answer is specific and avoids vague time references

    Retrieved Context:

    {{CONTEXT}}

    Question: {{QUESTION}}

    Answer:
    """


class RAGManager:
    def __init__(self, cfg: DictConfig, data_path="dataset/locomo10.json", chunk_size=500, k=1):
        self.cfg = cfg
        self.model = cfg.llm.model  # gpt-4.1-mini for generation
        self.embedding_model = cfg.openai.embedding_model
        self.llm_client = get_aoai_chat_completion_client(cfg)
        self.embedding_client = get_aoai_embedding_client(cfg)
        self.data_path = data_path
        self.chunk_size = chunk_size
        self.k = k

    def generate_response(self, question, context):
        template = Template(PROMPT)
        prompt = template.render(CONTEXT=context, QUESTION=question)

        max_retries = 3
        retries = 0

        while retries <= max_retries:
            try:
                t1 = time.time()
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that can answer questions based on the provided context."
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                )
                t2 = time.time()
                return response.choices[0].message.content.strip(), t2 - t1
            except Exception as e:
                retries += 1
                if retries > max_retries:
                    raise e
                time.sleep(1)  # Wait before retrying

    def clean_chat_history(self, chat_history):
        cleaned_chat_history = ""
        for c in chat_history:
            cleaned_chat_history += f"{c['timestamp']} | {c['speaker']}: {c['text']}\n"

        return cleaned_chat_history

    def calculate_embedding(self, document):
        response = self.embedding_client.embeddings.create(model=self.embedding_model, input=document)
        return response.data[0].embedding

    def calculate_similarity(self, embedding1, embedding2):
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

    def search(self, query, chunks, embeddings, k=1):
        """
        Search for the top-k most similar chunks to the query.

        Args:
            query: The query string
            chunks: List of text chunks
            embeddings: List of embeddings for each chunk
            k: Number of top chunks to return (default: 1)

        Returns:
            combined_chunks: The combined text of the top-k chunks
            search_time: Time taken for the search
        """
        t1 = time.time()
        query_embedding = self.calculate_embedding(query)
        similarities = [self.calculate_similarity(query_embedding, embedding) for embedding in embeddings]

        # Get indices of top-k most similar chunks
        if k == 1:
            # Original behavior - just get the most similar chunk
            top_indices = [np.argmax(similarities)]
        else:
            # Get indices of top-k chunks
            top_indices = np.argsort(similarities)[-k:][::-1]

        # Combine the top-k chunks
        combined_chunks = "\n<->\n".join([chunks[i] for i in top_indices])

        t2 = time.time()
        return combined_chunks, t2 - t1

    def create_chunks(self, chat_history, chunk_size=500):
        """
        Create chunks using tiktoken for more accurate token counting
        """
        # Get the encoding for the model
        encoding = tiktoken.encoding_for_model(self.embedding_model)

        documents = self.clean_chat_history(chat_history)

        if chunk_size == -1:
            return [documents], []

        chunks = []

        # Encode the document
        tokens = encoding.encode(documents)

        # Split into chunks based on token count
        for i in range(0, len(tokens), chunk_size):
            chunk_tokens = tokens[i : i + chunk_size]
            chunk = encoding.decode(chunk_tokens)
            chunks.append(chunk)

        embeddings = []
        for chunk in chunks:
            embedding = self.calculate_embedding(chunk)
            embeddings.append(embedding)

        return chunks, embeddings

    def process_all_conversations(self, output_file_path):
        data = load_data(self.data_path)

        FINAL_RESULTS = {}
        for idx, item in tqdm(enumerate(data), desc="Processing conversations", total=len(data)):
            # Get conversation ID from sample_id if available, otherwise use index
            key = item.get("sample_id", f"conversation_{idx}")

            # Extract all chat sessions and flatten them into a single chat history
            conversation = item["conversation"]
            chat_history = []

            # Iterate through all sessions
            session_idx = 1
            while f"session_{session_idx}" in conversation:
                session_chats = conversation[f"session_{session_idx}"]
                session_datetime = conversation.get(f"session_{session_idx}_date_time", "")

                # Add each chat in the session
                for chat in session_chats:
                    chat_with_timestamp = chat.copy()
                    if session_datetime and "timestamp" not in chat_with_timestamp:
                        chat_with_timestamp["timestamp"] = session_datetime
                    chat_history.append(chat_with_timestamp)

                session_idx += 1

            questions = item["qa"]

            chunks, embeddings = self.create_chunks(chat_history, self.chunk_size)

            FINAL_RESULTS[key] = []
            for qa_item in tqdm(questions, desc="Answering questions", leave=False):
                question = qa_item["question"]
                answer = qa_item.get("answer", "")
                category = str(qa_item["category"])

                if self.chunk_size == -1:
                    context = chunks[0]
                    search_time = 0
                else:
                    context, search_time = self.search(question, chunks, embeddings, k=self.k)
                response, response_time = self.generate_response(question, context)

                FINAL_RESULTS[key].append(
                    {
                        "question": question,
                        "answer": answer,
                        "category": category,
                        "context": context,
                        "response": response,
                        "search_time": search_time,
                        "response_time": response_time,
                    }
                )

            # Save after each conversation
            with open(output_file_path, "w+") as f:
                json.dump(FINAL_RESULTS, f, indent=4)

        # Final save
        with open(output_file_path, "w+") as f:
            json.dump(FINAL_RESULTS, f, indent=4)
