# build.py
import os
import shutil
import platform
import subprocess
import urllib.request
import urllib.error
import time
import tempfile
import hashlib
from datetime import datetime

from setuptools.command.build_py import build_py

def setup_proto_file():
    """Set up the proto file by downloading it from GitHub."""

    # Get the current directory and package directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.join(current_dir, 'segmentation_grpc')

    # Create directories if they don't exist
    os.makedirs(package_dir, exist_ok=True)

    # Target path (absolute)
    target = os.path.join(current_dir, 'segmentation.proto')

    # GitHub URL for the proto file
    github_url = 'https://raw.githubusercontent.com/jamesra/Viking_gRPC_protos/master/Segmentation/SAM2/segmentation.proto'

    # Check if we need to download the file
    need_download = True

    # If the file exists, check if it's been modified
    if os.path.exists(target) and os.path.isfile(target):
        try:
            # Download the remote file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name

            print(f"Downloading remote proto file to temporary location for comparison")
            urllib.request.urlretrieve(github_url, temp_path)

            # Calculate hashes for both files
            def get_file_hash(file_path):
                with open(file_path, 'rb') as f:
                    return hashlib.md5(f.read()).hexdigest()

            local_hash = get_file_hash(target)
            remote_hash = get_file_hash(temp_path)

            # Check if the files are different
            if local_hash != remote_hash:
                # Files are different, check if local file has been modified by user
                # We'll look for comments or other indicators that it's been manually edited
                with open(target, 'r') as f:
                    local_content = f.read()

                # Check for indicators of manual modification
                # This is a simple heuristic - you might want to improve it
                manual_edit_indicators = [
                    "// Modified by user",
                    "// Custom modification",
                    "// This is a modified version"
                ]

                is_manually_modified = any(indicator in local_content for indicator in manual_edit_indicators)

                if is_manually_modified:
                    print(f"Local file appears to be manually modified. Keeping local copy.")
                    need_download = False
                else:
                    # Get modification times for additional information
                    local_mtime = os.path.getmtime(target)
                    local_time = datetime.fromtimestamp(local_mtime)

                    # If the local file is newer than a reasonable threshold (e.g., 1 day),
                    # assume it's been intentionally modified
                    one_day_ago = time.time() - (24 * 60 * 60)
                    if local_mtime > one_day_ago:
                        print(f"Local file is recent (modified at {local_time}). Keeping local copy.")
                        need_download = False
                    else:
                        print(f"Local file differs from remote but doesn't appear to be manually modified.")
                        print(f"Local file will be replaced with the remote version.")
                        if os.path.islink(target) or os.path.isfile(target):
                            os.remove(target)
            else:
                # Files are identical, no need to download
                print(f"Local file is identical to remote file. No download needed.")
                need_download = False

            # Clean up the temporary file
            os.unlink(temp_path)

        except (urllib.error.URLError, ValueError, IOError) as e:
            print(f"Error checking remote file: {e}")
            # Keep the local file if we can't check the remote one
            print(f"Keeping local copy due to error checking remote file.")
            need_download = False

    # Download the proto file from GitHub if needed
    if need_download:
        try:
            print(f"Downloading proto file from {github_url}")
            urllib.request.urlretrieve(github_url, target)
            print(f"Successfully downloaded proto file to {target}")
            return True
        except urllib.error.URLError as e:
            print(f"Error downloading proto file: {e}")

            # Try to find a local copy as a fallback
            # Look in several possible locations
            possible_locations = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'external', 'Segmentation', 'SAM2', 'segmentation.proto'),
                os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'external', 'Segmentation', 'SAM2', 'segmentation.proto'),
                'external/Segmentation/SAM2/segmentation.proto'
            ]

            for local_source in possible_locations:
                if os.path.exists(local_source):
                    print(f"Falling back to local copy at {local_source}")
                    shutil.copy2(local_source, target)
                    print(f"Copied local proto file from {local_source} to {target}")
                    return True

            print(f"No local copy found in any of the expected locations")
            return False

    # If we get here, it means we didn't need to download and kept the local file
    return True


class CustomBuildCommand(build_py):
    """Custom build command to copy proto files before building."""

    def run(self):
        """Run the build command with proto file setup."""
        setup_proto_file()
        # Call the original build_py command
        super().run()


if __name__ == "__main__":
    # This allows running the script directly, not just as part of Poetry build
    setup_proto_file()
