"""
provenance_utils.py

Simulates a lightweight provenance/fingerprint scheme for document
authenticity. This models a realistic deployment pattern: a trusted feed
(NVD, MITRE-ATT&CK, a vendor) signs each document it publishes using a
private key. Anyone consuming the feed can verify the signature using the
corresponding public key, without needing to trust the document's content
on its own.

For this simulation we use HMAC-SHA256 with a shared secret instead of a
full public-key signature scheme (RSA/ECDSA). This keeps the defense
lightweight and dependency-free, appropriate for edge deployment, while
still demonstrating the core security property: an attacker who does not
possess the secret cannot produce a signature that verifies correctly.

In a production system, each trusted source would have its own keypair,
and the secret below would be replaced by proper asymmetric signing. That
upgrade path is noted in the paper's future work.
"""

import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

# Simulates the shared secret used by the trusted feed signing process.
# In production this would be a private key held only by the legitimate
# publisher (NVD, MITRE, the vendor), never by document consumers.
_TRUSTED_FEED_SECRET = os.environ.get("SECRET_KEY").encode("utf-8")


def sign_document(doc_text, source):
    """
    Produce a signature for a document, as if it had been signed at
    publication time by its trusted source.

    The signature covers both the text AND the source label together.
    This matters: it prevents an attacker from taking a legitimately
    signed document and just relabeling its source, since changing
    either the text or the source invalidates the signature.
    """
    message = f"{source}:{doc_text}".encode("utf-8")
    signature = hmac.new(_TRUSTED_FEED_SECRET, message, hashlib.sha256).hexdigest()
    return signature


def verify_document(doc_text, source, signature):
    """
    Recompute what the signature SHOULD be for this text+source pair,
    and check it against the signature actually attached to the
    document. Returns True only if they match exactly.

    hmac.compare_digest is used instead of == to prevent timing attacks
    (an attacker measuring how long comparison takes to guess the
    signature byte by byte). This is a standard cryptographic hygiene
    practice, not just a style choice.
    """
    expected_signature = sign_document(doc_text, source)
    return hmac.compare_digest(expected_signature, signature)