import os
import urllib.request
import os.path
import argparse
import json
import re
import sys
import textwrap

def download_asset(url, filename, token=None, verbose=False):
    headers = {}

    headers["Accept"] = 'application/octet-stream'
    if token:
        headers["Authorization"] = "token {}".format(token)

    if verbose:
        print( 'download url={}, headers={}'.format(url,headers) )
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            with open(filename, "wb") as fp:
                fp.write(response.read())
                print( "{}: OK".format(filename) )
    except urllib.error.HTTPError as e:
        print( 'HTTPError: {}'.format(e) )
        print( "{}: Error {}".format(filename,e) )

def get_assets(repo, re_assets=None, tag=None, token=None):
    if tag:
        url = "https://api.github.com/repos/{}/releases/tags/{}".format(repo, tag)
    else:
        url = "https://api.github.com/repos/{}/releases".format(repo)

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
                asset_url="{}?access_token={}".format(asset['url'], token) if token else asset['url']
                if re_assets is None:
                    yield (asset_url), asset['name']
                for re_asset in re_assets:
                    try:
                        if re.match(re_asset,asset['name']):
                            yield (asset_url), asset['name']
                    except re.error as e:
                        print( 'Invalid regular expression: {}'.format(re_asset) )
                        print( e )
                        return

def process_options(argv):
    if argv is None:
        argv = sys.argv[1:]
    description =	'download_github_assets.py supports downloading selected assets from github public and private repos.\n'
    epilog_fmt  =	'\nExamples:\n' \
                    'download_github_assets.py -a "*.mcs" -r slaclab/wave8\n'
    epilog = textwrap.dedent( epilog_fmt )
    parser = argparse.ArgumentParser( description=description, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog )
    parser.add_argument( '-a', '--assets',   dest='assets', action='append', \
                        help='Regex for assets to download. Ex: *.gz', default=[] )
    parser.add_argument( '-t', '--tags',     action="append", help='release tag to download.' )
    parser.add_argument( '-r', '--repo',	 action='store',  help='Github repo.  Ex. slaclab/wave8' )
    parser.add_argument( '-v', '--verbose',  action="store_true", help='show more verbose output.' )

    options = parser.parse_args( )
    return options 

def main(argv=None):
    options = process_options(argv)

    token_path = os.getenv('GH_TOKEN')
    token = None
    if token_path and os.path.isfile(token_path):
        with open(token_path) as f:
            token = f.read().strip()

    directory = '.'

    os.makedirs(directory, exist_ok=True)

    for tag in options.tags:
        assets = get_assets(repo=options.repo, re_assets=options.assets, tag=tag, token=token)
        for url, filename in assets:
            path = os.path.join(directory, filename)
            download_asset(url, filename, token)
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
