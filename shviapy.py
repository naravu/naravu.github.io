import subprocess

process = subprocess.Popen(["bash", "shviapy.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout, stderr = process.communicate()

print("Output:", stdout.decode())
print("Error:", stderr.decode())
