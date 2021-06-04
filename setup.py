from sys import platform
import subprocess

print (platform)
print ("Init Environment with production mode and start server...")
if platform == "linux" or platform == "darwin":
    subprocess.call("./lib/init/setup.sh")
elif platform == "win32" or platform == "win64":
    subprocess.call(r".\lib\init\setup.bat")
print ("done")