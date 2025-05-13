from generate_grpc import generate_grpc_code

try:
    from segmentation_pb2 import (SegmentationRequest,
                                  SegmentationResponse,
                                  Point, Polygon,
                                  SegmentationService)

    from segmentation_pb2_grpc import (SegmentationServiceServicer,
                                       SegmentationService)
except ModuleNotFoundError:
    # If the module is not found, it means the gRPC code has not been generated.
    # Attempt to generate the gRPC code. 
    if not generate_grpc_code(True):
        print("Failed to generate gRPC code. Please check the proto file.")
        raise
        
    from segmentation_pb2 import (SegmentationRequest,
                                  SegmentationResponse,
                                  Point, Polygon,
                                  SegmentationService)

    from segmentation_pb2_grpc import (SegmentationServiceServicer,
                                       SegmentationService)

