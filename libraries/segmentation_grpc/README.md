segmentation_grpc
======

This package compiles and supplies the gRPC interface for segmentation of images.

## Installation

```bash
pip install segmentation_grpc
```

During installation, the package automatically fetches the latest `segmentation.proto` file from the [Viking_gRPC_protos](https://github.com/jamesra/Viking_gRPC_protos) repository.

## Usage

After installation, you can generate the gRPC code using:

```bash
generate-grpc
```

This will create the necessary Python files for the gRPC interface based on the proto file.

## Development

If you're developing this package, you can run the build process manually:

```bash
python -m segmentation_grpc._build
```

This will download the proto file and place it in the correct location.
