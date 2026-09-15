"""
defense.py

The provenance-based defense against corpus poisoning.

Real-world deployment model:
    1. A trusted source (NVD, MITRE-ATT&CK, a vendor) signs each document
       at publication time, using a private key only they hold.
    2. When documents are ingested into the RAG system's corpus, the
       defense checks each one's signature before allowing it in.
    3. A poisoned document, lacking access to the trusted source's
       signing key, cannot produce a signature that passes verification,
       so it is rejected before it ever reaches the retriever.

This module provides two functions:
    - sign_legitimate_corpus: simulates the trusted publication step,
      attaching a valid signature to each legitimate document. This
      represents documents as they would already exist coming from a
      real signed feed, not something the RAG system itself does.
    - filter_verified_documents: the actual defense step. Given a mixed
      batch of documents (some signed, some not, some poisoned), returns
      only the ones that pass signature verification, and reports which
      were rejected and why.
"""

from provenance_utils import sign_document, verify_document


def sign_legitimate_corpus(documents):
    """
    Simulate documents arriving already signed by their trusted source.
    Returns new document dicts with a "signature" field added, leaving
    the originals untouched.
    """
    signed_docs = []
    for doc in documents:
        signature = sign_document(doc["text"], doc["source"])
        signed_doc = dict(doc)  # copy, don't mutate the original
        signed_doc["signature"] = signature
        signed_docs.append(signed_doc)
    return signed_docs


def filter_verified_documents(documents, verbose=True):
    """
    Given a list of documents, some of which may be poisoned and lack a
    valid signature, return only the documents that pass verification.

    A document is rejected if:
        - it has no "signature" field at all (e.g. a poisoned doc that
          never went through the trusted signing process), or
        - it has a "signature" field, but the signature doesn't match
          what verify_document computes for its actual text + source
          (e.g. a forged or stolen signature, or content that was
          altered after signing).
    """
    verified = []
    rejected = []

    for doc in documents:
        signature = doc.get("signature")

        if signature is None:
            rejected.append((doc, "no signature present"))
            continue

        if verify_document(doc["text"], doc["source"], signature):
            verified.append(doc)
        else:
            rejected.append((doc, "signature verification failed"))

    if verbose:
        print(f"[defense] {len(verified)} document(s) passed verification.")
        print(f"[defense] {len(rejected)} document(s) rejected:")
        for doc, reason in rejected:
            print(f"    - {doc['id']} (source={doc['source']}): {reason}")

    return verified