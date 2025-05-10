from segmentation_pb2 import (SegmentationRequest,
                              SegmentationResponse,
                              Point, Polygon,
                              SegmentationService)

from segmentation_pb2_grpc import (SegmentationServiceServicer,
                                   SegmentationService)

from generate_grpc import generate_grpc_code