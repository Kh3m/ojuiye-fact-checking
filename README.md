# OjuIye

OjuIye is a fact-checking system built to counter election disinformation
ahead of Nigeria's 2027 general elections. It checks claims against a
corpus of verified sources and returns a verdict along with the specific
source it relied on, rather than answering from general knowledge.

What makes it different from a typical fact-checking tool is provenance.
Every document in its corpus is cryptographically signed at the point it
enters the system, so a fabricated statement injected through a
compromised source or a spoofed website can be detected and rejected
automatically, rather than trusted just because it looks official.

OjuIye is a coined name. It is built around the Yoruba word "oju,"
meaning eye, and "Truth Eye" is the meaning intended for it, not a
literal Yoruba phrase.

## Why this project exists

Election disinformation in Nigeria spreads mainly through WhatsApp and
Facebook, often in Hausa, Yoruba, or Igbo, languages most existing
fact-checking tools do not cover well. This project is being built for
two purposes at once: as a real, deployable civic tool, and as the
applied case study behind an ongoing research project on provenance
defense for retrieval-augmented systems and multilingual retrieval for
low-resource African languages.

## Where this comes from

The provenance and signing mechanism used here was originally built and
tested in a separate project on RAG corpus poisoning defense for
cybersecurity assistants:
[rag-corpus-poisoning-iot-security](https://github.com/Kh3m/rag-corpus-poisoning-iot-security).
That project confirmed the defense works: a simulated corpus-poisoning
attack succeeded 3 out of 3 times without the signature check active,
and 0 out of 3 times with it active. OjuIye extends that same defense
into a real, multilingual, civic deployment.

## Current status

This project is under active development. Honest breakdown of what
exists right now versus what is planned:

**Working now:**
- Document signing and verification (HMAC-SHA256), carried over directly
  from the original research project
- A small real corpus of six documents, sourced from actual public INEC
  and Yiaga Africa statements
- Two independent retrieval backends, TF-IDF and a multilingual sentence
  embedding model (BAAI/bge-m3, chosen based on published benchmarks
  specifically for Yoruba, Igbo, and Hausa retrieval, rather than a
  general-purpose multilingual model)

**Not yet built, on the roadmap:**
- Combining the two retrieval backends into a single fused ranking,
  currently they run as interchangeable options, not in parallel
- WhatsApp intake and reply, via a Business Platform number
- OCR for image-based claims and transcription for voice notes
- A synthetic-media confidence flag for submitted images, using a
  third-party detector, not a system built from scratch
- Escalation to a human fact-checker when no verified source matches
- An observer dashboard tracking claims by state and language

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency
management.

```bash
uv sync
```

## Languages

English, Hausa, Yoruba, and Igbo.

## License

To be determined.