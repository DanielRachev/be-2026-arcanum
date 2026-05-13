"""Utility to extract public keys from PEM files."""

from __future__ import annotations

import sys

from .libsodium_bootstrap import ensure_libsodium


def extract_public_key_hex(pem_path: str) -> str:
    """
    Extract the Ed25519 public key from a PEM file and return it as hex.

    This is useful for sharing your public key with teammates.
    Requires libsodium to be available.
    """
    ensure_libsodium()

    from ipv8.keyvault.crypto import default_eccrypto

    try:
        with open(pem_path, "rb") as f:
            pem_data = f.read()
        key = default_eccrypto.key_from_private_bin(pem_data)
        pub_key_bin = key.pub().key_to_bin()
        return pub_key_bin.hex()
    except Exception as exc:
        raise ValueError(
            f"Failed to extract public key from '{pem_path}': {exc}"
        ) from exc


def print_public_key(pem_path: str) -> int:
    """CLI command to print public key from PEM file."""
    try:
        pubkey_hex = extract_public_key_hex(pem_path)
        print(pubkey_hex)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
