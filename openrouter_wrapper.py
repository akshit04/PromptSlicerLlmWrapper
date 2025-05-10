import requests
import tiktoken

class OpenRouterWrapper:
    def __init__(self, api_key, model="mistralai/mistral-7b-instruct", max_tokens=4000):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def num_tokens(self, text):
        return len(self.encoding.encode(text))

    def chat(self, messages, temperature=0.7, max_tokens=1000):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def split_text_into_chunks(self, text, max_chunk_tokens=2000):
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            current_text = " ".join(current_chunk)
            if self.num_tokens(current_text) > max_chunk_tokens:
                current_chunk.pop()
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def process_large_prompt(self, user_prompt):
        chunks = self.split_text_into_chunks(user_prompt)
        overall_summarized_context = ""
        running_context = []
        results = []

        for i, chunk in enumerate(chunks):
            prompt = f"""
You are reading a large document split into chunks.
Here is chunk {i+1}/{len(chunks)}:
{chunk}

Previous context:
{overall_summarized_context}

Please analyze this chunk in light of the previous context.
"""
            messages = [
                {"role": "system", "content": "You are a smart assistant that reads the provided software code, and provide the detailed explanation of what business purpose the code is providing and how different components are connected, and ineracting with each other."},
                {"role": "user", "content": prompt}
            ]
            response = self.chat(messages, temperature=0.3, max_tokens=1000)
            results.append(response.strip())

            context_messages = [
                {"role": "system", "content": "You are a smart assistant that summarizes the given content below within 1000 words so that it can be used as a context for remaining analysis."},
                {"role": "user", "content": response.strip()}
            ]
            overall_summarized_context = self.chat(context_messages, temperature=0.3, max_tokens=1000)
            running_context.append(overall_summarized_context)

        return {
            "final_summary": overall_summarized_context,
            "individual_context_summaries": running_context,
            "individual_results": results,
        }