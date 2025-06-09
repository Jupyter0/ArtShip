import subprocess
import sys
import signal
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Run Django server and Q cluster together"

    def handle(self, *args, **options):
        print("[Auto] Starting Django Q cluster...")

        # Use Windows-specific process group flag
        if os.name == 'nt':  # Windows
            q = subprocess.Popen(
                [sys.executable, 'manage.py', 'qcluster'],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:  # Unix/Linux/Mac
            q = subprocess.Popen(
                [sys.executable, 'manage.py', 'qcluster'],
                preexec_fn=os.setsid
            )

        def stop_qcluster():
            if q.poll() is None:
                print("[Auto] Stopping Q cluster...")
                try:
                    if os.name == 'nt':
                        q.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        os.killpg(os.getpgid(q.pid), signal.SIGINT)
                except Exception as e:
                    print("[Error] Could not stop Q cluster:", e)
                q.wait()
                print("[Auto] Q cluster stopped.")

        try:
            # Run Django's normal runserver, passing any flags
            call_command('runserver', *args, **options)
        except KeyboardInterrupt:
            print("[Auto] Ctrl-C received. Shutting down...")
        finally:
            stop_qcluster()
