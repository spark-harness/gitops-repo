FROM golang:1.26-bookworm AS builder

ARG JANUS_REPO=https://github.com/spark-harness/janus.git
ARG JANUS_REF=master
ARG BUF_VERSION=1.47.2

WORKDIR /src
COPY janus/ /src/janus/
RUN test -f /src/janus/go.mod || { rm -rf /src/janus && git clone --depth 1 --branch "${JANUS_REF}" "${JANUS_REPO}" janus; }
WORKDIR /src/janus
RUN go build -trimpath -ldflags="-s -w" -o /out/janus ./cmd/janus
RUN go install "github.com/bufbuild/buf/cmd/buf@v${BUF_VERSION}" \
  && cp /go/bin/buf /out/buf

FROM debian:bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates curl git jq maven openjdk-17-jdk-headless openssh-client python3 unzip \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/go /usr/local/go
COPY --from=builder /out/janus /usr/local/bin/janus
COPY --from=builder /out/buf /usr/local/bin/buf
COPY prepare_maven_version.py /usr/local/bin/prepare_maven_version.py

RUN chmod +x /usr/local/bin/prepare_maven_version.py
RUN ln -sf /usr/local/go/bin/go /usr/local/bin/go \
  && ln -sf /usr/local/go/bin/gofmt /usr/local/bin/gofmt

ENV PATH="/usr/local/go/bin:${PATH}"

ENTRYPOINT ["/bin/bash", "-lc"]
CMD ["janus version"]
