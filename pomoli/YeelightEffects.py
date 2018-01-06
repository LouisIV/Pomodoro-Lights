# Yeelight.py

import yeelight
from yeelight import transitions as trans


def build_bulb(bulb, yee_effect):
    port = 55443
    if 'port' in bulb:
        port = bulb['port']

    effect = 'sudden'
    if 'effect' in yee_effect:
        effect = yee_effect['effect']
    elif 'effect' in bulb:
        effect = bulb['effect']

    duration = 500
    if 'duration' in yee_effect:
        duration = yee_effect['duration']
    elif 'duration' in bulb:
        duration = bulb['duration']

    auto_on = True
    if 'auto_on' in yee_effect:
        auto_on = yee_effect['auto_on']
    elif 'auto_on' in bulb:
        auto_on = bulb['auto_on']

    return yeelight.Bulb(
        ip=bulb['ip'],
        port=port,
        effect=effect,
        duration=duration,
        auto_on=auto_on,
    )


def handle_effect(settings, effects):
    print("effects: %s" % len(effects))
    for yee_effect in effects:
        if 'type' in yee_effect:
            print("found")

            bulbs = []
            if 'group' in yee_effect:
                for bulb in settings:
                    if 'group' in bulb and bulb['group'] is \
                       yee_effect['group']:
                            bulbs.append(build_bulb(bulb, yee_effect))
            elif 'bulb_name' in yee_effect:
                for bulb in settings:
                    if 'name' in bulb and bulb['name'] is \
                       yee_effect['bulb_name']:
                            bulbs.append(build_bulb(bulb, yee_effect))
            else:
                for bulb in settings:
                    bulbs.append(build_bulb(bulb, yee_effect))

            if yee_effect['type'] == "pulse":
                color = yee_effect['color']

                pulses = 2
                if yee_effect['pulses']:
                    pulses = yee_effect['pulses']

                pulse(bulbs, color, pulses)
            if yee_effect['type'] == "steady":
                rgb(bulbs, yee_effect['color'])


def hex_color_to_rgb(color):
    """Convert a hex color string to an RGB tuple."""
    color = color.strip("#")
    try:
        red, green, blue = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    except (TypeError, ValueError):
        red, green, blue = (255, 0, 0)
    return red, green, blue


def rgb(bulbs, hex_color):
    """Set the RGB value of the bulb."""
    red, green, blue = hex_color_to_rgb(hex_color)
    for bulb in bulbs:
        bulb.set_rgb(red, green, blue)


def pulse(bulbs, hex_color, pulses):
    """Pulse the bulb in a specific color."""
    red, green, blue = hex_color_to_rgb(hex_color)
    transitions = trans.pulse(red, green, blue)

    for bulb in bulbs:
        # Get the initial bulb state.
        if bulb.get_properties().get("power", "off") == "off":
            action = yeelight.Flow.actions.off
        else:
            action = yeelight.Flow.actions.recover

        bulb.start_flow(yeelight.Flow(count=pulses, action=action,
                                      transitions=transitions))
