#!/usr/bin/env python
"""
Custom script to generate fumadocs JSON for python-binance.
This handles the mismatch between module name (binance) and package name (python-binance).
"""

import json
import griffe
from importlib.metadata import version as get_version
from griffe_typingdoc import TypingDocExtension
import fumapy

# Monkey-patch the version function to handle the binance -> python-binance mapping
original_version = get_version


def patched_version(name):
    if name == "binance":
        return original_version("python-binance")
    return original_version(name)


def main():
    # Patch the version function in the document_module
    import fumapy.mksource.document_module as dm

    dm.version = patched_version

    # Load the module using griffe with extensions
    extensions = griffe.load_extensions(TypingDocExtension)
    module = griffe.load(
        "binance", docstring_parser="auto", store_source=True, extensions=extensions
    )

    # Parse using fumadocs
    result = fumapy.mksource.parse_module(module)

    # Write to JSON file using the custom encoder
    with open("binance.json", "w") as f:
        json.dump(result, f, cls=fumapy.mksource.CustomEncoder, indent=2)

    print(f"✓ Generated binance.json successfully")
    print(f"  Version: {result.get('version', 'unknown')}")
    print(f"  Modules: {len(result.get('modules', {}))}")
    print(f"  Classes: {len(result.get('classes', {}))}")
    print(f"  Functions: {len(result.get('functions', {}))}")


if __name__ == "__main__":
    main()
