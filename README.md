# healthchecks-action

healthchecks action for creating+pinging the api.

## inputs

| **input**      | **description**                                                                                                                        | **valid inputs**                   | **needed for** |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | -------------- |
| baseurl        | url of the healthchecks instance                                                                                                       | {str} _(with http(s)://)_          | create + ping  |
| apikey         | api write key for check creation                                                                                                       | {str}                              | create         |
| check_name     | name for the check                                                                                                                     | {str}                              | create         |
| check_schedule | schedule for the check                                                                                                                 | {str} _(in cron format)_           | create         |
| grace          | grace time for the check"                                                                                                              | {int}                              | create         |
| path           | path to ping after {baseurl}/ping/                                                                                                     | {str}                              | ping           |
| method         | ping method (after ping path)                                                                                                          | `start`\| `fail`\| `log`\| {empty} | ping           |
| succeeded      | if the action succeeded. can be used instead of `method` to signal success or failure. but be aware that `succeeded` takes precedence. | `start`\| `fail`\| `log`\| {empty} | ping           |
| ping_body      | content to add to ping body                                                                                                            | {str}                              | ping           |

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
    healthchecks:
        runs-on: ubuntu-latest
        steps:
            - name: create check
              uses: olofvndrhr/healthchecks-action@v1
              with:
                  baseurl: https://hc.example.com
                  apikey: "${{ secrets.APIKEY }}"
                  check_name: check1
                  check_schedule: "5 * * * *"
                  grace: 600

            - name: start check
              uses: olofvndrhr/healthchecks-action@v1
              with:
                  baseurl: https://hc.example.com
                  path: xxxxxx
                  method: start

            - name: stop check
              uses: olofvndrhr/healthchecks-action@v1
              with:
                  baseurl: https://hc.example.com
                  path: xxxxxx

            - name: stop check (with succeeded)
              uses: olofvndrhr/healthchecks-action@v1
              with:
                  baseurl: https://hc.example.com
                  path: xxxxxx
                  succeeded: ${{ success() }}

            - name: fail check
              if: ${{ failure()
              uses: olofvndrhr/healthchecks-action@v1
              with:
                  baseurl: https://hc.example.com
                  path: xxxxxx
                  method: fail
                  ping_body: some error message

            - name: fail check (with succeeded)
              if: ${{ failure() || success() }}
              uses: olofvndrhr/healthchecks-action@v1
              with:
                  baseurl: https://hc.example.com
                  path: xxxxxx
                  succeeded: ${{ success() }}
                  ping_body: some error message
```
