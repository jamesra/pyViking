"""
Setup script for the SegmentationServer package.
"""

from setuptools import setup, find_packages

setup(
    name="segmentation_server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "protobuf",
        "numpy",
        "pillow",
        "opencv-python",
        "torch",
        "sam2",
        "segmentation_grpc",
    ],
    python_requires=">=3.13",
    description="Server for the Viking segmentation service",
    author="James Anderson",
    entry_points={
        "console_scripts": [
            "segmentation-server=segmentation_server.__main__:main",
        ],
    },
)