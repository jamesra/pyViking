from .generate_grpc import generate_grpc_code

try:
    from  . import segmentation_pb2
    from .segmentation_pb2 import (SegmentationRequest,
                                  SegmentationResponse,
                                  SegmentResult,
                                  Point, Polygon)

    from . import segmentation_pb2_grpc
    from .segmentation_pb2_grpc import (SegmentationServiceServicer,
                                        add_SegmentationServiceServicer_to_server,
                                            SegmentationService)
except ModuleNotFoundError:
    # If the module is not found, it means the gRPC code has not been generated.
    # Attempt to generate the gRPC code.
    print("gRPC code not found. Attempting to generate it.")
    try:
        if not generate_grpc_code(True):
            print("Failed to generate gRPC code. Please check the proto file.")
            raise ImportError("Failed to generate gRPC code")
    except ModuleNotFoundError as e:
        if "grpc_tools" in str(e):
            print("Warning: grpc_tools not found. Cannot generate gRPC code.")
            print("Please install grpcio-tools and run 'python -m segmentation_grpc' to generate the gRPC code.")
            raise ImportError("grpc_tools not found. Please install grpcio-tools") from e
        else:
            raise

    # Try to import again after generating the code
    try:
        from . import segmentation_pb2
        from .segmentation_pb2 import (SegmentationRequest,
                                       SegmentationResponse,
                                       Point, Polygon)

        from . import segmentation_pb2_grpc
        from .segmentation_pb2_grpc import (SegmentationServiceServicer,
                                            SegmentationService)
    except ModuleNotFoundError:
        print("Failed to import generated gRPC code even after attempting to generate it.")
        print("This might be because grpcio-tools is not installed or the proto file is invalid.")
        raise
