# SoftAware: Visual Software Health Check for GitHub Repositories

## CW24 Hack Day project by Team Violet

 Team members:
 * Sadie Bartholomew
 * Adam Ward
 * James Byrne
 * Anne Barber

## Backend usage 

Set up a personal access token for github API
  - repo:status
  - repo_deployment
  - public_repoAccess
  - repo:invite
  - read:user

Make sure this is available in GITHUB_API_TOKEN for script usage

```commandline
export GITHUB_AUTH_TOKEN=...
```

Then run the script which will plonk some JSON to standard out, so you can redirect that straight to a file

```commandline
./create_json.sh data/<a text file with a list of repos in user/repo form>
```

