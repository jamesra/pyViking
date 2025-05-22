#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

# Import the proto file setup function
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _build import setup_proto_file

class CustomBuildCommand(build_py):
    """Custom build command to set up proto files and generate gRPC code before building."""

    def run(self):
        """Run the build command with proto file setup and gRPC code generation."""
        setup_proto_file()

        try:
            import generate_grpc
            print("Importing generate_grpc module")
        except ModuleNotFoundError:
            # If the module is not found, we can still run the generate_grpc_code function
            pass

        generate_grpc.generate_grpc_code()  # Force regeneration of gRPC code
        # Call the original build_py command
        super().run()



setup(
    name="segmentation_grpc",
    version="0.1.0",
    description="gRPC interface for the segmentation service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="James Anderson",
    python_requires=">=3.13",
    packages=find_packages(),
    package_data={
        "segmentation_grpc": ["*.proto", "*.py"],
    },
    include_package_data=True,
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "protobuf",
    ],
    entry_points={
        "console_scripts": [
            "generate-grpc=segmentation_grpc.generate_grpc:generate_grpc_code",
        ],
    },
    cmdclass={
        "build_py": CustomBuildCommand,
    },
)
