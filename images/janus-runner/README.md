# Janus Runner Image

This image provides the fixed toolchain used by Spark Argo repository gates.

It contains:

- `janus`
- `git`
- `gh`
- `buf`
- Go toolchain
- JDK 17 and Maven
- HTTPS Git support through tokens
- `curl`
- `jq`
- `python3`
- `bash`

The builder stage uses Go 1.26 because current Janus source requires
`go >= 1.26`.

Build example:

```bash
rsync -a --delete --exclude .git ../../janus/ images/janus-runner/janus/
docker build \
  --build-arg JANUS_REF=master \
  -t registry.cn-shenzhen.aliyuncs.com/love-is-pain/janus-runner:LEN-54-bootstrap-20260623-1608 \
  images/janus-runner
```

Cluster build example:

```bash
rsync -a --delete --exclude .git ../../janus/ images/janus-runner/janus/
docker buildx build \
  --platform linux/amd64 \
  --build-arg JANUS_REF=master \
  -t registry.cn-shenzhen.aliyuncs.com/love-is-pain/janus-runner:LEN-54-bootstrap-20260623-1608 \
  --push \
  images/janus-runner
```

Do not bake repository tokens or cluster credentials into this image. Argo
Workflows inject credentials through Kubernetes Secrets.
