#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path


def main() -> int:
    java_version = os.environ["JAVA_VERSION"]
    pom = Path("pom.xml")
    text = pom.read_text(encoding="utf-8")
    text, version_count = re.subn(
        r"(<artifactId>spark-idl-java</artifactId>\s*\n\s*<version>)[^<]+",
        rf"\g<1>{java_version}",
        text,
        count=1,
    )
    if version_count != 1:
        print("Could not update spark-idl-java project version.", file=sys.stderr)
        return 1

    gencode_versions = []
    for source in Path("src/main/java").rglob("*.java"):
        header = source.read_text(encoding="utf-8", errors="ignore")[:300]
        match = re.search(r"Protobuf Java Version:\s*([0-9]+)\.([0-9]+)\.([0-9]+)", header)
        if match:
            gencode_versions.append(tuple(int(part) for part in match.groups()))

    if gencode_versions:
        protobuf_version = ".".join(str(part) for part in max(gencode_versions))
        text, protobuf_count = re.subn(
            r"(<protobuf-java\.version>)[^<]+(</protobuf-java\.version>)",
            rf"\g<1>{protobuf_version}\g<2>",
            text,
            count=1,
        )
        if protobuf_count != 1:
            print("Could not update protobuf-java.version.", file=sys.stderr)
            return 1

    pom.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
