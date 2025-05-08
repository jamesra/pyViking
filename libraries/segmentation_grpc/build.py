# build.py
import os
import shutil
import platform
import subprocess

def setup_proto_file():
    """Set up the proto file by first trying to create a symbolic link,
    then falling back to copying if that fails."""

    # Create directories if they don't exist
    os.makedirs('segmentation_grpc', exist_ok=True)

    # Source and target paths
    source = 'external/Viking_gRPC_protos/Segmentation/SAM2/segmentation.proto'
    target = 'segmentation_grpc/segmentation.proto'

    # Make sure the source file exists
    if not os.path.exists(source):
        print(f"Error: Source file {source} not found. Make sure the Git submodule is initialized.")
        print("Run: git submodule update --init --recursive")
        return

    # Remove existing link or file if it exists
    if os.path.exists(target):
        if os.path.islink(target) or os.path.isfile(target):
            os.remove(target)

    symlink_created = False

    # Try to create a symbolic link based on the platform
    try:
        if platform.system() == 'Windows':
            # Windows requires different approaches based on permissions
            try:
                # Create symlink (requires admin privileges or developer mode)
                subprocess.run(['mklink', target, os.path.abspath(source)],
                               shell=True,
                               check=True,
                               stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE)
                symlink_created = True
                print(f"Successfully created symbolic link to {source}")
            except subprocess.CalledProcessError:
                # If mklink fails, we'll fall back to copying
                pass
        else:
            # Unix-like systems (Linux, macOS)
            relative_path = os.path.relpath(source, os.path.dirname(target))
            os.symlink(relative_path, target)
            symlink_created = True
            print(f"Successfully created symbolic link to {source}")
    except (OSError, subprocess.SubprocessError) as e:
        print(f"Warning: Failed to create symbolic link: {e}")

    # Fall back to copying if symlink creation failed
    if not symlink_created:
        shutil.copy2(source, target)
        print(f"Symbolic link creation failed, copied {source} to {target} instead")

def build(setup_kwargs):
    """This function is mandatory for poetry to build the package."""
    setup_proto_file()

    # Include the proto files in the package
    if 'package_data' not in setup_kwargs:
        setup_kwargs['package_data'] = {}
    setup_kwargs['package_data']['segmentation_grpc'] = ['*.proto']

    return setup_kwargs

if __name__ == "__main__":
    # This allows running the script directly, not just as part of Poetry build
    setup_proto_file()