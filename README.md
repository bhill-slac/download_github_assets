# download_github_assets

<!--- ######################################################## -->

# Environment: python3

```
Usage:
  python download_github_assets.py  -a '\S*.mcs' -r slaclab/wave8 -t v2.1.1 -d 2.1.1
  python download_github_assets/download_github_assets.py  -a '\S*.mcs' -r slaclab/cameralink-gateway -t v1.15.0 -d v1.15.0
```

Note: In order to download assets from a private github repo, you'll need a github
personal access token.
> https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token


Create a file w/ the personal access token and make it mode 0600 so it's private.
A good location is your ~/.ssh folder which is typically 0700 and thus private.
Set your env variable GITHUB_TOKEN_PATH to the path to your personal access token file.
Note that if you use verbose mode, your token will be printed to stdout.
