import os
from JsonConfig import JsonConfig
from PomodoroTimer import PomodoroTimer


def main():
    config = JsonConfig(os.path.expanduser('~/.config/pomoli/pomoli.json'))
    if config:
        pomo_timer = PomodoroTimer(config.get_file())
        pomo_timer.clock()
    else:
        print("Configuration file was not valid.")


if __name__ == '__main__':
    main()
