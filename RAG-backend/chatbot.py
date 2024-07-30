import os
import torch
import re
import subprocess
from transformers import AutoTokenizer, AutoModelForCausalLM, GPTQConfig, pipeline, BitsAndBytesConfig
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from energy_measurement import get_gpu_metrics
import requests
from util.utils import clean_references
from flask import Flask, jsonify, request

app = Flask(__name__)

model = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model, device="auto")
model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=model,
                                                 #token=GEMMA_TOKEN,
                                                 torch_dtype=torch.float16,
                                                 device_map = "auto"
                                                 )

embedding_function = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={'device':"cuda"}
        )

# path = "/home/jupyter-robelamare2016/experiments/gemma-RAG/data/docs_2/test_db"
path = "/RAG-backend/database/db"
vectordb = Chroma(persist_directory=path,
                                  embedding_function=embedding_function)

text_generation_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)




@app.route("/prompt", methods = ['POST'])
def prompt():
    
    data = request.json
    
    docs = vectordb.similarity_search(data['messages'], k=2)
    
    question = "# Prompt that you have to answer:\n" + data['messages']
    question1 = data['messages']
    retrieved_content, markdown_documents = clean_references(docs)

    llm_system_role_without_history = "In the following you recieve a prompt. Answer it based on given content. Provide only the response, dont say 'Answer:'.",

    prompt_wrapper = f"{llm_system_role_without_history}\n\n{question}\n\n{retrieved_content}"
    
    prompt_wrapper1 = f"{question1}\n\n{retrieved_content}"
    system_prompt = '''You are an intelligent assistant on sustainability that provides an explanation and detailed information on sustainability indicators and goals for Freiburg City. Respond in the same language as the query. If the query is in German, reply in German. If the query is in English, reply in English. Use the provided documents to inform your response.If the requested value is 0 or not available, kindly suggest to contact The city administration and call  0761 2010.'''
    
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": {prompt_wrapper1}},
]
    prompt = text_generation_pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    outputs = text_generation_pipeline(
        prompt,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.1,
        top_k=50,
        top_p=0.95
    )
    
    
    torch.cuda.empty_cache()
    gpu_data = get_gpu_metrics()
    if not data or 'messages' not in data:
            return jsonify({"error": "Missing 'messages' in request"}),400
    output = {"response": outputs[0]["generated_text"][len(prompt):], "gpu_data":gpu_data}
    #return jsonify({"response": outputs[0]["generated_text"][len(prompt):]})
    return jsonify(output)

if __name__ == "__main__":
#   add a host and port to run the app
  app.run(host="123.123.123.123", port=36000)
