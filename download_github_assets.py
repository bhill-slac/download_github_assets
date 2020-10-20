import os
import urllib.request
import os.path
import json

def download_asset(url, filename, token=None):
    headers = {}
    
    headers["Accept"] = 'application/octet-stream'
    if token:
        headers["Authorization"] = "token {}".format(token)

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        with open(filename, "wb") as fp:
            fp.write(response.read())

def get_assets(owner, repo, tag=None, token=None):
    if tag:
        url = "https://api.github.com/repos/{}/{}/releases/tags/{}".format(owner, repo, tag)
    else:
        url = "https://api.github.com/repos/{}/{}/releases".format(owner, repo)

    headers = {}
    if token:
        headers["Authorization"] = "token {}".format(token)
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        content = json.load(response)
        if tag:
            tags = [content]
        else:
            tags = content
        
        for tag_data in tags:
            for asset in tag_data['assets']:
                yield ("{}?access_token={}".format(asset['url'], token) if token else asset['url']), asset['name']

if __name__ == '__main__':
    owner='REPO_OWNER'
    repo='REPO_NAME'
    token = 'PRIVATE_ACCESS_TOKEN OPETIONAL'
    tags = [
        'RELEASE_TAGS_CONTAININGP_ASSETS'
    ]

    directory = '.'

    os.makedirs(directory, exist_ok=True)

    for tag in tags:
        assets = get_assets(owner=owner, repo=repo, token=token)
        for url, filename in assets:
            path = os.path.join(directory, filename)
            download_asset(url, filename)

