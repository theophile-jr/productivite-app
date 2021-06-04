from sys import platform
import subprocess

print (platform)
print ("Init Environment with production mode and start server...")
if platform == "linux" or platform == "darwin":
    subprocess.call("./lib/init/setup.sh")
else:
    subprocess.call("./lib/init/setup.bat")
print ("done")