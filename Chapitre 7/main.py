import signal
import sys

def signal_handler(sig, frame):
    print(' Ctrl+C!')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    print('Ctrl+C pour quitter.')
    while True:
        pass

if __name__ == "__main__":
    main()