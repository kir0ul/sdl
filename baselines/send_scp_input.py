from pathlib import Path
import sys
from paramiko import SSHClient
from scp import SCPClient

# Remote server credentials
hostname = "cs-gpu1.cs.uml.edu"
port = 22
username = "apierre"
password = "k:6:K]mK"


def progress4(filename, size, sent, peername):
    sys.stdout.write(
        "(%s:%s) File `%s`: %.2f%%   \r"
        % (
            peername[0],
            peername[1],
            Path(str(filename)).absolute(),
            float(sent) / float(size) * 100,
        )
    )
    sys.stdout.write("\n")


# File paths
local_file_path = Path("sample.txt")
remote_path = Path("~/") / local_file_path

# Create a sample file to transfer
with open(local_file_path, "w") as fid:
    fid.write("Hello from local machine!")


with SSHClient() as ssh:
    ssh.load_system_host_keys()
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    print(f"Connected to `{hostname}`")

    with SCPClient(ssh.get_transport(), progress4=progress4) as scp:
        scp.put(local_file_path, remote_path=remote_path)
        # scp.get(
        #     "test/Theory of Segmentation -- Koloydenko, Alexey.pdf",
        # )
        # scp.put('test', recursive=True, remote_path=remote_path)


local_file_path.unlink()
