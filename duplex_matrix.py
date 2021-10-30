import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import MatrixScanner, DiodeOrientation, intify_coordinate
from kmk.hid import HIDModes

class DuplexMatrixScanner:
    def __init__(
        self,
        cols,
        rows
    ):
        """Constructor

        Args:
            cols: list of col_pins
            rows: list of row_pins

        Example:
            If arguments are belows:
                cols = (PIN1, PIN2)
                rows = (PIN3, PIN4)
            then, the keymap definition (and wirings) looks like this:
                [
                #   PIN1  PIN2
                    key1, key2,     # PIN3 (COL2ROW)
                    key3, key4,     # PIN4 (COL2ROW)
                    key5, key6,     # PIN3 (ROW2COL)
                    key7, key8      # PIN4 (ROW2COL)
                ]
        """
        self.len_cols = len(cols)
        self.len_rows = len(rows)

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) == self.len_cols + self.len_rows
        ), 'Cannot use a pin as both a column and row'
        del unique_pins

        self.io_cols = [
            x
            if x.__class__.__name__ == 'DigitalInOut'
            else digitalio.DigitalInOut(x)
            for x in cols
        ]
        self.io_rows = [
            x
            if x.__class__.__name__ == 'DigitalInOut'
            else digitalio.DigitalInOut(x)
            for x in rows
        ]

        self.len_state_arrays = self.len_cols * self.len_rows * 2
        self.state = bytearray(self.len_state_arrays)
        self.report = bytearray(3)

    def scan_for_changes(self):
        '''
        Poll the matrix for changes and return either None (if nothing updated)
        or a bytearray (reused in later runs so copy this if you need the raw
        array itself for some crazy reason) consisting of (row, col, pressed)
        which are (int, int, bool)
        '''
        ba_idx = 0
        any_changed = False
        row_index_offset = 0

        for diode_orientation in (DiodeOrientation.COLUMNS, DiodeOrientation.ROWS):
            if diode_orientation == DiodeOrientation.COLUMNS:
                outputs = self.io_cols
                inputs = self.io_rows
            elif diode_orientation == DiodeOrientation.ROWS:
                outputs = self.io_rows
                inputs = self.io_cols
            for oidx, opin in enumerate(outputs):
                opin.switch_to_output(value=True)

                for iidx, ipin in enumerate(inputs):
                    ipin.switch_to_input(pull=digitalio.Pull.DOWN)

                    # cast to int to avoid
                    #
                    # >>> xyz = bytearray(3)
                    # >>> xyz[2] = True
                    # Traceback (most recent call last):
                    #   File "<stdin>", line 1, in <module>
                    # OverflowError: value would overflow a 1 byte buffer
                    #
                    # I haven't dived too far into what causes this, but it's
                    # almost certainly because bool types in Python aren't just
                    # aliases to int values, but are proper pseudo-types
                    new_val = int(ipin.value)
                    old_val = self.state[ba_idx]

                    if old_val != new_val:
                        # self.report: [row, col, is_pressed]
                        if diode_orientation == DiodeOrientation.COLUMNS:
                            self.report[0] = iidx
                            self.report[1] = oidx
                        elif diode_orientation == DiodeOrientation.ROWS:
                            self.report[0] = oidx
                            self.report[1] = iidx
                        # offset row index for duplex matrix tables
                        self.report[0] += row_index_offset

                        self.report[2] = new_val
                        self.state[ba_idx] = new_val

                        any_changed = True
                        break

                    ba_idx += 1

                opin.value = False
                if any_changed:
                    break

            if any_changed:
                break
            row_index_offset += len(self.io_rows)

        if any_changed:
            return self.report


class KMKKeyboardDuplexMatrix(KMKKeyboard):
    matrix_scanner = DuplexMatrixScanner

    def _init_sanity_check(self):
        '''
        Ensure the provided configuration is *probably* bootable
        '''
        assert self.keymap, 'must define a keymap with at least one row'
        assert self.row_pins, 'no GPIO pins defined for matrix rows'
        assert self.col_pins, 'no GPIO pins defined for matrix columns'
        # skip diode_orientation check
        assert (
            self.hid_type in HIDModes.ALL_MODES
        ), 'hid_type must be a value from kmk.consts.HIDModes'

        return self

    def _init_coord_mapping(self):
        '''
        Attempt to sanely guess a coord_mapping if one is not provided. No-op
        if `kmk.extensions.split.Split` is used, it provides equivalent
        functionality in `on_bootup`

        To save RAM on boards that don't use Split, we don't import Split
        and do an isinstance check, but instead do string detection
        '''
        if any(x.__class__.__module__ == 'kmk.modules.split' for x in self.modules):
            return

        if not self.coord_mapping:
            self.coord_mapping = []

            rows_to_calc = len(self.row_pins)
            cols_to_calc = len(self.col_pins)

            for dup in range(2):
                for ridx in range(rows_to_calc):
                    for cidx in range(cols_to_calc):
                        new_ridx = ridx + rows_to_calc * dup
                        self.coord_mapping.append(intify_coordinate(new_ridx, cidx))

    def _init_matrix(self):
        self.matrix = DuplexMatrixScanner(
            cols=self.col_pins,
            rows=self.row_pins
        )
        return self