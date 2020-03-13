# GitHub Action for Neural Style Transfer on Images

<!-- [![Actions Status](https://github.com/Akshay090/github-action-neural-style-transfer/workflows/Lint/badge.svg)](https://github.com/Akshay090/github-action-neural-style-transfer/actions) -->
[![Actions Status](https://github.com/Akshay090/github-action-neural-style-transfer/workflows/Integration%20Test/badge.svg)](https://github.com/Akshay090/github-action-neural-style-transfer/actions)

## Usage

Example usage of action in your workflow

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action
      uses: Akshay090/github-action-neural-style-transfer@master
      with:
        path: tests/sample_image.jpg
    - uses: actions/upload-artifact@v1
      with:
        name: styled_image
        path: styled_output
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `path`  | Path to text file to be summarized    |

