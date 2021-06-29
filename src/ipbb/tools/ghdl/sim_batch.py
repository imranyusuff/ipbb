
import tempfile
import sh
import sys

from os.path import join, split, exists, splitext, basename
from ...utils import which
#from .sim_common import autodetect, ModelSimNotFoundError, _vsim, _vcom
from .sim_common import GHDLNotFoundError

# -----------------------------------------------------------------------------
class GHDLBatch(object):
    """docstring for GHDLBatch"""

    # --------------------------------------------
    def __init__(self, scriptpath=None, echo=False, log=None, cwd=None, dryrun=False):
        super().__init__()

        self.scriptpath = scriptpath
        self.log = log
        self.terminal = sys.stdout if echo else None
        self.cwd = cwd
        self.dryrun = dryrun

    # --------------------------------------------
    def __enter__(self):
        self.script = (
            open(self.scriptpath, 'w')
            if self.scriptpath
            else tempfile.NamedTemporaryFile(mode='w+t', suffix='.do')
        )
        return self

    # --------------------------------------------
    def __exit__(self, type, value, traceback):
        if not self.dryrun:
            self._run()
        self.script.close()

    # --------------------------------------------
    def __call__(self, *strings):
        for f in [self.script, self.terminal]:
            if not f:
                continue
            f.write(' '.join(strings) + '\n')
            f.flush()

    # --------------------------------------------
    def _run(self):

        # Guard against missing ghdl executable
        if not which('ghdl'):
            raise GHDLNotFoundError(
                #"'%s' not found in PATH. Failed to detect GHDL" % _vsim
                "ghdl not found in PATH. Failed to detect GHDL" % _vsim
            )

        # TODO not implmented yet for GHDL!
        #vsim = sh.Command(_vsim)
        # TODO:

        #lRoot, _ = splitext(basename(self.script.name))

        #lLog = self.log if self.log else 'transcript_{}.log'.format(lRoot)

        #vsim(
        #    '-c',
        #    '-l',
        #    lLog,
        #    '-do',
        #    self.script.name,
        #    '-do',
        #    'quit',
        #    _out=sys.stdout,
        #    _err=sys.stderr,
        #    _cwd=self.cwd,
        #)
