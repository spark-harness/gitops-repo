# CI Workflow Entrypoints

保存由 GitHub Actions 或 Argo Events 触发的 workflow 入口。

第一期建议由 GitHub Actions 触发 Argo Workflow 并等待结果，再把 GitHub Actions job 作为 required check。
