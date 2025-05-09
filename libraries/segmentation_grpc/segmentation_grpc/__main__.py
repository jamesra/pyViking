"""
Main entry point for the segmentation_grpc package.

This module allows running the package as a Python module:
python -m segmentation_grpc
"""

import sys
import argparse
from segmentation_grpc.generate_grpc import generate_grpc_code

def main(*args):
    """Main entry point for the segmentation service."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Compile gRPC code for the segmentation service.')
    parser.add_argument('--force', action='store_true',
                        help='Regenerate gRPC code even if it already exists')
    args = parser.parse_args()

    """Generate the gRPC code when the package is run as a module."""
    print("Generating gRPC code...")
    if generate_grpc_code(args.force):
        print("gRPC code generation successful.")
        return 0
    else:
        print("gRPC code generation failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())