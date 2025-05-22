import urllib.request
import urllib.error

url = 'https://raw.githubusercontent.com/jamesra/Viking_gRPC_protos/master/Segmentation/SAM2/segmentation.proto'
try:
    with urllib.request.urlopen(url) as response:
        print(f"URL is accessible. Status code: {response.status}")
        print(f"Content length: {len(response.read())} bytes")
except urllib.error.URLError as e:
    print(f"Error accessing URL: {e}")