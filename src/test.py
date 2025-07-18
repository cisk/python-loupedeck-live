import time
import logging
import sys

from Loupedeck import DeviceManager

logging.basicConfig(level=logging.DEBUG)

devices = DeviceManager().enumerate()

knob_name = 'knobTL'
knob_value = 0.0
knob_old_value = 0.0
knob_last_time_ns = 0


def callback(obj, event=None):
    global knob_name, knob_value, knob_old_value
    # if event is not None:
    #     # print(f">> {obj=} >> {value=}")
    # else:
    #     print(f">> {obj=}")
    if event['id'] == knob_name:
        _act_value = event['ts']
        _state = event['state']
        if knob_old_value == 0:
            knob_old_value = _act_value
            knob_last_time_ns = time.time_ns()
        else:
            _delta = _act_value - knob_old_value
            knob_old_value = _act_value
            if _state == 'left':
                knob_value -= _delta
            elif _state == 'right':
                knob_value += _delta
            else:
                raise ValueError
    print(f">> {event=} >> {knob_value=}")

# if len(devices) > 0:
#     l = devices[0]
#     print("trying..", l)
#     l.test()
#     time.sleep(5)
#     l.stop()

if len(devices) > 0:
    l = devices[0]
    print("trying..", l)
    l.set_callback(callback)
    l.test()
    _gate = True
    while _gate:
        try:
            sys.stdin.read()
        except KeyboardInterrupt:
            _gate = False
            l.stop()
    
    