# LEN-51 Image Release Review

## Scope

- Repository: `gitops-repo`
- Branch: `feature/LEN-51-image-release-strategy`
- Base: `origin/master`
- Ticket: `LEN-51`

## Traceability

- AC1 is covered by `github-image-release` PR tag generation: `pr-<pr-number>-<short-sha>`.
- AC2 is covered by Trivy scanning with non-zero exit on `HIGH` or `CRITICAL` findings and GitHub status failure on workflow failure.
- AC3 is covered by GitOps overlay digest fields and `promote=true` digest update flow.

## Contract Compatibility

No protobuf, HTTP API, event schema, or generated contract files changed.

## Security And Operations

- No secret values are committed.
- The workflow references Kubernetes Secrets by name only.
- BuildKit rootless is selected as the default builder.
- The builder still requires `privileged: true` until a hardened builder runtime exists on `vincent-k3s`.

## Validation

- `kubectl kustomize workflows/templates`
- `kubectl kustomize workflows/ci`
- `kubectl kustomize apps/applicant-api/overlays/sta1`
- `kubectl kustomize apps/applicant-api/overlays/sta2`
- `kubectl kustomize apps/applicant-api/overlays/prod`
- PyYAML parsed all `*.yaml`.
- `git diff --check`
- `kubectl --kubeconfig ~/.kube/vincent-k3s.yaml --context vincent-k3s apply --server-side --dry-run=server -k workflows/templates`
- `kubectl --kubeconfig ~/.kube/vincent-k3s.yaml --context vincent-k3s apply --server-side --dry-run=server -k workflows/ci`

## Residual Risk

The image workflow has not been executed end-to-end because no business repository webhook/Sensor and registry Secret are installed in this slice.

Conclusion: ready-for-gate for the GitOps template and policy slice.
