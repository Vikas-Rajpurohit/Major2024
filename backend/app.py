from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)

# Set up Gemini API with your API key
genai.configure(api_key=os.environ["API_KEY"])

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

    def dfs(folder_url, indent, file, file_names, folder_names):
        if folder_url in visited_links:
            return
        visited_links.add(folder_url)

        driver.get(folder_url)
        page_source = driver.page_source
        folder_soup = BeautifulSoup(page_source, 'html.parser')
        folder_links = folder_soup.select('a.Link--primary:not([class*=" "])')

        for link in folder_links[::2]:
            name = link.get_text()

            if '.' in name:
                file_names.append(name)
            else:
                folder_names.append(name)
                file_structure[name] = {'files': [], 'folders': []}
                dfs(folder_url + '/' + name, indent + 1, file,
                    file_structure[name]['files'], file_structure[name]['folders'])

    driver.get(repo_url)
    visited_links.add(repo_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    file_links = soup.select('a.Link--primary:not([class*=" "])')

    file_structure['root'] = {'files': [], 'folders': []}

    for link in file_links[::2]:
        name = link.get_text()
        if '.' in name:
            file_structure['root']['files'].append(name)
        else:
            file_structure['root']['folders'].append(name)
            file_structure[name] = {'files': [], 'folders': []}
            dfs(repo_url + '/tree/master/' + name, 1, None,
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


if __name__ == '__main__':
    app.run(debug=True)
