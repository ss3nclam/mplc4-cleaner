import subprocess


class System:

    @staticmethod
    def run_cmd(command: str):
        return subprocess.run(
            args = command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True,
            text = True
            )


    @staticmethod
    def get_diskspace_usage() -> int:
        cmd = r"sudo df -B1 -T /boot | awk '{print $6}' | grep -E '[0-9]+'"
        shell = System.run_cmd(cmd)

        return int(shell.stdout.rstrip('%\n'))