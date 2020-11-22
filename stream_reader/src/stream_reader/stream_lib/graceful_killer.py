import signal


class GracefulKiller:
    """
    From https://stackoverflow.com/a/31464349/11540608

    Fargate should send SIGTERM when the task is being stopped. We then have around 30 seconds to clean up and exit
    gracefully before being forcefully killed.
    """
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True
