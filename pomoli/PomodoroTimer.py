# PomodoroTimer.py
from datetime import datetime, timedelta
from time import sleep
import YeelightEffects

NOW = datetime.now


class PomodoroTimer():
    def __init__(self, configuration):
        if configuration is None:
            raise ValueError("You need to provide a configuration file.")

        self.configuration = configuration

        times = None
        if 'times' in self.configuration:
            times = self.configuration['times']

        cycle = None
        if 'cycle' in self.configuration:
            cycle = self.configuration['cycle']

        if None in (times, cycle):
            raise ValueError("You need to update your configuration file.")

        events_to_remove = []
        for x in range(0, len(cycle)):
            if cycle[x] not in times:
                print("One or more of your events may not be formated"
                      + "correctly: ", end='')
                events_to_remove.append(x)

        new_cycle = []
        if len(events_to_remove) > 0:
            for x in range(0, len(cycle)):
                if x in events_to_remove:
                    print(cycle[x], end=' ')
                else:
                    new_cycle.append(cycle[x])
            print("\nThese event(s) will be skipped.")
            cycle = new_cycle

        self.times = times
        self.cycle = cycle

        self.effects = {}
        if 'effects' in self.configuration:
            self.effects = self.configuration['effects']
            print("Found some effects!")

        self.effect_settings = None

        self.current_cycle = cycle
        self.current_action = None

        self.current_duration = None
        self.start_time = None
        self.end_time = None

    """
    ###############################################
    * * * * * * * * * YEELIGHT * * * * * * * * * *
    ###############################################
    """
    def _setup_yeelight(self):
        if 'yeelight_settings' in self.configuration:
            self.effect_settings['yeelight_settings'] \
                = self.configuration['yeelight_settings']
        else:
            print("If you would like to use Yeelights please add them to"
                  + "the configuration file.")
            self.effect_settings['yeelight_settings'] = "Missing"

    def _handle_yeelight_effect(self, event, effect):
        if 'yeelight_settings' in self.effect_settings:
            if self.effect_settings['yeelight_settings'] is not "Missing":
                YeelightEffects.handle_effect(
                    self.effect_settings['yeelight_settings'],
                    effect)
            else:
                pass
        else:
            self._setup_yeelight()
            self._handle_effect(event)

    """
    ###############################################
    * * * * * * * * * EFFECTS * * * * * * * * * *
    ###############################################
    """

    def _handle_effect(self, event):
        if not self.effect_settings:
            self.effect_settings = {}
        if self.effects:
            if event in self.effects:
                for effect in self.effects[event]:
                    print("Processing effects for %s" % event)
                    if effect in 'yeelight':
                        self._handle_yeelight_effect(
                            event, self.effects[event][effect])

    def _pomodoro(self):
        if len(self.current_cycle) < 1:
            self.current_cycle = self.cycle

        self.current_duration = self.times[self.current_cycle[0]]
        self.start_time = datetime.now()
        self.end_time = datetime.now() + timedelta(
            minutes=self.current_duration
        )
        print("Starting %s at %s. Ending at %s." % (
            self.current_cycle[0],
            self.start_time.strftime("%H:%M"),
            self.end_time.strftime("%H:%M"))
        )
        self._handle_effect(self.current_cycle[0])
        self.current_cycle.pop(0)

    def clock(self):
        self._pomodoro()
        while True:
            sleep(self.current_duration * 60)
            self._pomodoro()
