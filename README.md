## Requirements
This project makes the following assumptions.
### auth0
algorithms=["RS256"]

## Setup
### Environment Variables #FIXME

## Example Application
This is based on: [coreycothrum/fastapi_template](https://github.com/coreycothrum/fastapi_template).

Do all [setup](#setup) from previous section.

### SSL Certificates
Follow [these instructions](https://github.com/coreycothrum/nginx_certbot_docker_compose#initial-setup) to setup HTTPS certificates.

This is needed even for development. [Auth0](https://auth0.com/) needs a domain to redirect to. HTTPS should be a requirement here.

## Contributing
Rules for working in/with this repo.

### Use Conventional Commits
Git commits should adhere to the [conventional commits spec](https://www.conventionalcommits.org/).

### Use `pre-commit`
Keep the repo clean, use [pre-commit](https://pre-commit.com/).

1. Install [pre-commit](https://pre-commit.com/#1-install-pre-commit).

2. Apply [pre-commit](https://pre-commit.com/#3-install-the-git-hook-scripts) config to local git hook script(s):

        pre-commit install
        pre-commit install --hook-type commit-msg

3. (optional, as needed) Update [pre-commit](https://pre-commit.com/#pre-commit-autoupdate) config to latest:

        pre-commit autoupdate

4. (optional, as needed) Manually run [pre-commit](https://pre-commit.com/#pre-commit-run) check(s):

        pre-commit run --all-files
