# PyTorch Project Config

## Data Sources
- source: https://github.com/pytorch/pytorch
  type: github
  fetcher: pytorch-community-mcp
  scope: [pr, issue, rfc, commits, key-contributors]

- source: https://dev-discuss.pytorch.org/
  type: discourse
  fetcher: pytorch-community-mcp
  scope: [discussions]

- source: https://pytorch.org/blog/
  type: website
  fetcher: pytorch-community-mcp
  scope: [blog]

- source: pytorch-events
  type: events
  fetcher: pytorch-community-mcp
  scope: [events]

- source: pytorch-slack
  type: slack
  fetcher: pytorch-community-mcp
  scope: [slack-threads]

## Repository Context
- primary_repo: pytorch/pytorch
- related_repos:
  - repo: pytorch/vision
    role: related
  - repo: pytorch/audio
    role: related
  - repo: pytorch/xla
    role: related
  - repo: Ascend/pytorch
    role: downstream
    url: https://gitcode.com/Ascend/pytorch

## Version Mapping
- project_ref: main
  repo_refs:
    - repo: pytorch/pytorch
      ref: main

- project_ref: v2.7.1
  repo_refs:
    - repo: pytorch/pytorch
      ref: v2.7.1

## Local Cache Policy
- local_analysis_enabled: true
- repo_cache_dir: .cache/openinsight/repos
- worktree_dir: .cache/openinsight/worktrees
- default_branch: main

