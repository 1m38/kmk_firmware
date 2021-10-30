import supervisor

supervisor.set_next_stack_limit(4096 + 4096)


import storage
import board
import digitalio

def storage_control(pin_in, pin_out=None, pull=digitalio.Pull.UP):
    """Disable USB Drive if the switch is pressed when power on.

    Args:
        pin_in: pin name for input
        pin_out: pin name for output
        pull: PullUp/PullDown for input pin
    """

    io_in = digitalio.DigitalInOut(pin_in)
    io_in.switch_to_input(pull=pull)
    io_out = None
    if pin_out is not None:
        io_out = digitalio.DigitalInOut(pin_out)
        if pull == digitalio.Pull.UP:
            io_out.switch_to_output(value=False)
        elif pull == digitalio.Pull.DOWN:
            io_out.switch_to_output(value=True)

    if io_in.value:
        storage.disable_usb_drive()

    io_in.deinit()
    if io_out is not None:
        io_out.deinit()

storage_control(board.GP3, board.GP6, digitalio.Pull.UP)
