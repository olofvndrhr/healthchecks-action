# healthchecks-action

healthchecks action for creating+pinging the api.

## inputs

| **input**      | **description**                    | **valid inputs**            | **needed for** |
| -------------- | ---------------------------------- | --------------------------- | -------------- |
| baseurl        | url of the healthchecks instance   | {str} _(with http(s)://)_   | create + ping  |
| apikey         | api write key for check creation   | {str}                       |                |
| check_name     | name for the check                 | {str}                       |                |
| check_schedule | schedule for the check             | {str} _(in cron format)_    |                |
| grace          | grace time for the check"          | {int}                       |                |
| path           | path to ping after {baseurl}/ping/ | {str}                       |                |
| method         | ping method (after ping path)      | `/start`\| `/fail`\| {none} |                |

## outputs

> none

## how to use

```yml
name: generate release notes

on:
    push:
        tags:
            - "v*.*.*"

jobs:
    get-release-notes:
        runs-on: ubuntu-latest
        steps:
            - name: checkout code
              uses: actions/checkout@v3

            - name: get release notes
              id: get-releasenotes
              uses: olofvndrhr/releasenote-gen@v1
              with:
                  version: latest # default
                  changelog: CHANGELOG.md # default
                  releasenotes: RELEASENOTES.md # default

            - name: get release notes for ref
              uses: olofvndrhr/releasenote-gen@v1
              with:
                  version: ${{ github.ref_name }} # name of the pushed tag

            # use the generated release notes string for further steps
            - name: print release notes
              run: echo "${{ steps.get-releasenotes.outputs.releasenotes }}"
```
