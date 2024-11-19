from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from flask_cors import CORS
import os
import asyncio
from llama_index.core import ServiceContext
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
import google.generativeai as genai
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core import Settings
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.core.storage.storage_context import StorageContext
# from llama_index.llm_providers import HuggingFaceInferenceAPI
# from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
# from llama_index.legacy.embeddings.langchain import LangchainEmbedding

load_dotenv()
app = Flask(__name__)
CORS(app)
# Set up Gemini API with your API key
genai.configure(api_key=os.environ["API_KEY"])

Settings.chunk_size = 512
# executor = ThreadPoolExecutor()

# HF_TOKEN = "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"
# llm = HuggingFaceInferenceAPI(
#     model_name="HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN
# )

# embed_model = LangchainEmbedding(
#     HuggingFaceInferenceAPIEmbeddings(
#         api_key=HF_TOKEN, model_name="thenlper/gte-large")
# )
# Settings.llm = llm
# Settings.embed_model = embed_model

# Selenium setup
options = Options()
options.add_argument("--headless")
options.add_argument("--profile-directory=Default")

service = Service(
    "C:/Users/user/Downloads/chromedriver-win64/chromedriver.exe")


def scrape_github_repo(repo_url):
    visited_links = set()
    file_structure = {}

    driver = webdriver.Chrome(service=service, options=options)

    def dfs(folder_url, indent, file_names, folder_names):
        if folder_url in visited_links:
            return
        visited_links.add(folder_url)

        driver.get(folder_url)
        page_source = driver.page_source
        folder_soup = BeautifulSoup(page_source, 'html.parser')
        folder_links = folder_soup.select('a.Link--primary:not([class*=" "])')

        for link in folder_links[::2]:
            name = link.get_text().strip()

            if '.' in name:
                file_names.append(name)
            else:
                folder_names.append(name)
                file_structure[name] = {'files': [], 'folders': []}
                dfs(folder_url + '/' + name, indent + 1,
                    file_structure[name]['files'], file_structure[name]['folders'])

    driver.get(repo_url)
    visited_links.add(repo_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    file_structure['root'] = {'files': [], 'folders': []}
    file_links = soup.select('a.Link--primary:not([class*=" "])')

    for link in file_links[::2]:
        name = link.get_text().strip()
        if '.' in name:
            file_structure['root']['files'].append(name)
        else:
            file_structure['root']['folders'].append(name)
            file_structure[name] = {'files': [], 'folders': []}
            dfs(repo_url + '/tree/master/' + name, 1,
                file_structure[name]['files'], file_structure[name]['folders'])

    driver.quit()

    return file_structure


# API endpoint to scrape GitHub repo folder structure
@app.route('/get-folder-structure', methods=['POST'])
def get_folder_structure():
    try:
        # Get the repo URL from the request body
        data = request.get_json()
        repo_url = data.get('repo_url')

        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400

        # Scrape the folder structure
        folder_structure = scrape_github_repo(repo_url)

        return jsonify({'folder_structure': folder_structure}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/describe-folder', methods=['POST'])
def describe_folder():
    try:
        data = request.get_json()
        folder_structure = data.get('folder_structure')

        if not folder_structure:
            return jsonify({'error': 'Folder structure is required'}), 400

        descriptions = []

        # Iterate through each folder in the structure
        for folder, contents in folder_structure.items():
            folder_names = contents['files'] + \
                contents['folders']  # Merge files and folders

            # Create prompt for each folder
            prompt = f"Generate a concise description for a folder containing items like: {
                folder_names}"

            # Generate description using Gemini model
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Collect the description with the folder name
            descriptions.append({
                'folder_name': folder,
                'description': response.text.strip()
            })

        return jsonify({'descriptions': descriptions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Asynchronous function to create the knowledge graph


# def create_knowledge_graph(docs):
    try:
        # Log before creating the index
        print("Starting the creation of the knowledge graph index...")

        # Create the knowledge graph index
        graph_store = SimpleGraphStore()
        storage_context = StorageContext.from_defaults(graph_store=graph_store)

        index = KnowledgeGraphIndex.from_documents(
            documents=docs,
            max_triplets_per_chunk=3,
            storage_context=storage_context,
            include_embeddings=True
        )

        # Log after creating the index
        print("Knowledge graph index created successfully.")

        # Persist the processed data
        storage_context.persist(persist_dir='./storage')
        print("Data persisted to './storage'")

    except Exception as e:
        print(f"Error occurred during knowledge graph creation: {e}")


@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        # Check if 'file' is part of the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        print(f"File received: {file.filename}")  # Logging: File received

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Check if file is actually received
        if not file:
            return jsonify({'error': 'File is required'}), 400

        # Read file content and log it
        file_content = file.read().decode('utf-8')
        # Log first 100 characters for validation
        print(f"File content received: {file_content[:100]}...")

        # Process the file into documents
        reader = SimpleDirectoryReader(input_files=['../github.txt'])
        docs = reader.load_data()
        # Create the knowledge graph and index using updated Settings
        settings = Settings(chunk_size=256)

        # executor.submit(create_knowledge_graph, docs)

        # Return success response immediately
        # return jsonify({'message': 'File processed and knowledge graph creation started'}), 200

        graph_store = SimpleGraphStore()
        storage_context = StorageContext.from_defaults(graph_store=graph_store)

        # Log before creating the index
        print("Starting the creation of the knowledge graph index...")

        index = KnowledgeGraphIndex.from_documents(
            documents=docs,
            max_triplets_per_chunk=3,
            storage_context=storage_context,
            # settings=settings,  # Use the new Settings object
            # include_embeddings=True
        )

        # Log after creating the index
        print("Knowledge graph index created successfully.")

        # Store the processed data
        storage_context.persist(persist_dir='./storage')
        print("Data persisted to './storage'")

        return jsonify({'message': 'File processed and knowledge graph created successfully'}), 200

    except Exception as e:
        # Log the error with more details
        print(f"Error occurred: {e}")
        return jsonify({'error': ''}), 500

# API 2: Query the knowledge graph based on stored information


@app.route('/query-knowledge', methods=['POST'])
def query_knowledge():
    try:
        query = request.json.get('query')

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Rebuild storage context and load the index
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = KnowledgeGraphIndex.load_index_from_storage(storage_context)

        query_engine = index.as_query_engine(
            include_text=True,
            response_mode="tree_summarize",
            embedding_mode="hybrid",
            similarity_top_k=5
        )

        # Use Gemini to fetch answers
        prompt = f"""<|system|>Please check if the following pieces of context have any mention of the keywords provided in the Question. If not, then say that you don't know. Please don’t make up an answer.</s>
        <|user|>Question: {query}
        Helpful Answer:</s>"""

        response = query_engine.query(prompt)
        return jsonify({'response': response.response.split("<|assistant|>")[-1].strip()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
