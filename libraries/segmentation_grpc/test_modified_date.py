import os
import time
import shutil
from segmentation_grpc._build import setup_proto_file

# Path to the proto file
current_dir = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(current_dir, 'segmentation_grpc', 'segmentation.proto')

# Create a backup of the existing file if it exists
if os.path.exists(target):
    backup_path = target + '.bak'
    print(f"Backing up existing proto file to {backup_path}")
    shutil.copy2(target, backup_path)

# Create a modified version of the proto file
print(f"Creating a modified version of the proto file at {target}")
with open(target, 'w') as f:
    f.write("""syntax = "proto3";

package segmentation;

// This is a modified version of the proto file
// It should be kept if it's newer than the remote copy

service SegmentationService {
  rpc SegmentImage (SegmentationRequest) returns (SegmentationResponse) {}
}

message SegmentationRequest {
  bytes image_data = 1;
  int32 width = 2;
  int32 height = 3;
}

message SegmentationResponse {
  bytes labeled_image = 1;
  int32 width = 2;
  int32 height = 3;
}
""")

# Set the modification time to now (which should be newer than the remote file)
os.utime(target, (time.time(), time.time()))
print(f"Set modification time of {target} to now")

# Run the setup_proto_file function
print("\nRunning setup_proto_file function...")
setup_proto_file()

# Check if the file was kept or replaced
print("\nChecking if the file was kept or replaced...")
with open(target, 'r') as f:
    content = f.read()
    if "This is a modified version of the proto file" in content:
        print("SUCCESS: The modified file was kept!")
    else:
        print("FAILURE: The modified file was replaced!")

# Restore the backup if it exists
if os.path.exists(backup_path):
    print(f"\nRestoring backup from {backup_path}")
    shutil.copy2(backup_path, target)
    os.remove(backup_path)