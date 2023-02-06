import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ['GITLAB_ACCESS_TOKEN']
USER_ID = os.environ['GITLAB_USER_ID']
REPO_IDS_TO_NOT_DELETE = json.loads(os.environ['REPO_IDS_TO_NOT_DELETE'])

def main(): 
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    get_projects_url = f'https://gitlab.com/api/v4/users/{USER_ID}/projects?per_page=9999'

    all_repos_response = requests.get(get_projects_url, headers=headers)
    all_repos_response.raise_for_status()

    for repo in all_repos_response.json():
        if repo['id'] not in REPO_IDS_TO_NOT_DELETE:
            repo_id = repo['id']
            repo_name = repo['name']

            print(f'Deleting repo with: \nid = {repo_id} \ntitle = {repo_name}')

            delete_project_url = f'https://gitlab.com/api/v4/projects/{repo["id"]}'
            requests.delete(delete_project_url, headers=headers)

            print('')
    
    print('Done!')

if __name__ == '__main__':
    main()
