import logging
import subprocess


class System:

    _logs_owner: str = __qualname__

    @staticmethod
    def run_cmd(command: str):
        return subprocess.run(
            args=command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        )

    @staticmethod
    def get_diskspace_usage():
        cmd = r"sudo df -B1 -T /boot | awk '{print $6}' | grep -E '[0-9]+'"

        try:
            shell = System.run_cmd(cmd)
            out: str = shell.stdout.rstrip("\%\n")

            if not out.isdigit() or not int(out) in range(101) or shell.stderr:
                raise_msg = "ошибка выполнения команды"
                shell_error_msg = ": " + shell.stderr.rstrip("\n")

                raise SystemError(f"{raise_msg}{shell_error_msg}")

            return int(out)

        except Exception as error:
            logging.warning(
                f"{System._logs_owner}: не удалось получить данные об использовании носителя: {error}"
            )

            return
