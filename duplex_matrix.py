import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import MatrixScanner, DiodeOrientation, intify_coordinate
from kmk.hid import HIDModes

class DuplexMatrixScanner:
    def __init__(
        self,
        cols,   # list of lists of col_pins
        rows,   # list of lists of row_pins
        diode_orientations=(DiodeOrientation.COLUMNS, DiodeOrientation.ROWS)
    ):
        """Constructor

        Args:
            cols: list of lists of col_pins (dimensions of all lists of col_pins must be the same)
            rows: list of lists of row_pins
            diode_directions: list of diode directions

        Example:
            If arguments are belows:
                cols = [[PIN1, PIN2], [PIN1, PIN2]],
                rows = [[PIN3, PIN4], [PIN3, PIN4]],
                diode_directions = [DiodeOrientation.COLUMNS, DiodeOrientation.ROWS]
            then, the keymap definition (and wirings) looks like this:
                [
                #   PIN1  PIN2
                    key1, key2,     # PIN3 (COL2ROW)
                    key3, key4,     # PIN4 (COL2ROW)
                    key5, key6,     # PIN3 (ROW2COL)
                    key7, key8      # PIN4 (ROW2COL)
                ]
        """
        assert len(cols) == len(rows) == len(diode_orientations), "cols, rows and diode_orientations must be the same"

        self.lens_cols = (len(l) for l in cols)
        self.lens_rows = (len(l) for l in rows)

        # A pin cannot be both a row and column, detect this by combining the
        # two tuples into a set and validating that the length did not drop
        #
        # repr() hackery is because CircuitPython Pin objects are not hashable
        for c, r in zip(cols, rows):
            unique_pins = {repr(p) for p in c} | {repr(p) for p in r}
            assert (
                len(unique_pins) == len(c) + len(r)
            ), 'Cannot use a pin as both a column and row'
            del unique_pins

        self.diode_orientations = diode_orientations

        for o in self.diode_orientations:
            assert o in (DiodeOrientation.COLUMNS, DiodeOrientation.ROWS), "Invalid DiodeOrientation {}".format(o)

        ios = {}
        for cols_or_rows in (cols, rows):
            for pins in cols_or_rows:
                for pin in pins:
                    if repr(pin) in ios.keys():
                        continue
                    ios[repr(pin)] = digitalio.DigitalInOut(pin)
        self.ios_cols = [
            [ ios[repr(pin)] for pin in pins ]
            for pins in cols
        ]
        self.ios_rows = [
            [ ios[repr(pin)] for pin in pins ]
            for pins in rows
        ]

        self.len_state_arrays = sum(c * r for c, r in zip(self.lens_cols, self.lens_rows))
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

        for io_cols, io_rows, diode_orientation in zip(self.ios_cols, self.ios_rows, self.diode_orientations):
            if diode_orientation == DiodeOrientation.COLUMNS:
                outputs = io_cols
                inputs = io_rows
            elif diode_orientation == DiodeOrientation.ROWS:
                outputs = io_rows
                inputs = io_cols
            else:
                raise ValueError("Invalid DiodeOrientation {}".format(diode_orientation))
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
                        else:
                            raise ValueError("Invalid DiodeOrientation {}".format(diode_orientation))
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
            row_index_offset += len(io_rows)

        if any_changed:
            return self.report


class KMKKeyboardDuplexMatrix(KMKKeyboard):
    diode_orientations = None
    matrix_scanner = DuplexMatrixScanner
    rows_pins = None
    cols_pins = None

    def _init_sanity_check(self):
        '''
        Ensure the provided configuration is *probably* bootable
        '''
        assert self.keymap, 'must define a keymap with at least one row'
        assert self.rows_pins, 'no GPIO pins defined for matrix rows'
        assert self.cols_pins, 'no GPIO pins defined for matrix columns'
        # assert self.diode_orientation is not None, 'diode orientation must be defined'
        assert self.diode_orientations is not None, 'diode orientations must be defined'
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
            row_index_offset = 0

            for row_pins, col_pins in zip(self.rows_pins, self.cols_pins):
                for ridx in range(len(row_pins)):
                    for cidx in range(len(col_pins)):
                        self.coord_mapping.append(intify_coordinate(ridx + row_index_offset, cidx))
                row_index_offset += len(row_pins)

    def _init_matrix(self):
        self.matrix = DuplexMatrixScanner(
            cols=self.cols_pins,
            rows=self.rows_pins,
            diode_orientations=self.diode_orientations
        )
        return self