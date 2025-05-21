#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

# Import the proto file setup and gRPC code generation functions
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _build import setup_proto_file
from generate_grpc import generate_grpc_code

class CustomBuildCommand(build_py):
    """Custom build command to set up proto files and generate gRPC code before building."""
    
    def run(self):
        """Run the build command with proto file setup and gRPC code generation."""
        # Set up the proto file (download or use local copy)
        setup_proto_file()
        
        # Generate gRPC code from the proto file
        generate_grpc_code(force=True)
        
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
        "segmentation_grpc": ["*.proto"],
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