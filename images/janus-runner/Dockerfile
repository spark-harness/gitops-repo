FROM golang:1.26-bookworm AS builder

ARG JANUS_REPO=https://github.com/spark-harness/janus.git
ARG JANUS_REF=master
ARG BUF_VERSION=1.47.2
ARG MAVEN_VERSION=3.9.11

WORKDIR /src
COPY janus/ /src/janus/
RUN test -f /src/janus/go.mod || { rm -rf /src/janus && git clone --depth 1 --branch "${JANUS_REF}" "${JANUS_REPO}" janus; }
WORKDIR /src/janus
RUN go build -trimpath -ldflags="-s -w" -o /out/janus ./cmd/janus
RUN go install "github.com/bufbuild/buf/cmd/buf@v${BUF_VERSION}" \
  && cp /go/bin/buf /out/buf

FROM eclipse-temurin:21-jdk-jammy

ARG MAVEN_VERSION=3.9.11

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates curl git jq openssh-client python3 unzip \
  && curl -fsSL "https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz" \
    | tar -xz -C /opt \
  && ln -sf "/opt/apache-maven-${MAVEN_VERSION}/bin/mvn" /usr/local/bin/mvn \
  && mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg -o /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends gh \
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
