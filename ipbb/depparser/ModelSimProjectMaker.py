from __future__ import print_function
import time
import os

from Pathmaker import Pathmaker
from os.path import join, split, exists, splitext, abspath
from ..tools.common import SmartOpen

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class ModelSimProjectMaker(object):
    # --------------------------------------------------------------
    def __init__(self, aReverse = False, aTurbo=True):
        self.reverse = aReverse
        self.turbo = aTurbo
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    def write(self, aTarget, aScriptVariables, aComponentPaths, aCommandList, aLibs, aMaps):

        # ----------------------------------------------------------
        # FIXME: Tempourary assignments
        write = aTarget
        lWorkingDir = abspath(join(os.getcwd(), 'top'))
        # ----------------------------------------------------------

        # ----------------------------------------------------------

        write('# Autogenerated project build script')
        write(time.strftime('# %c'))
        write()
        write('onerror { quit -code 255 }')

        for setup in aCommandList['setup']:
            write('source {0}'.format(setup.FilePath))

        write('vlib work')

        for lib in set(aLibs):
            write('vlib {0}'.format(lib))

        for ma in aMaps:
            write('vmap {0} {1}'.format(ma[0], ma[1]))
            write('vcom -work {0} -refresh -force_refresh'.format(ma[0]))

        lSrcs = aCommandList['src'] if not self.reverse else reversed(aCommandList['src'])


        lSrcCommandGroups = []
        # ----------------------------------------------------------
        for src in lSrcs:

            # ----------------------------------------------------------
            if src.Include:

                lPath, lBasename = split(src.FilePath)
                lName, lExt = splitext(lBasename)
                lMap = src.Map

                # ----------------------------------------------------------
                if lExt == '.xco':
                    file = abspath(join(lPath, lName + '.vhd'))
                elif lExt == '.xci':
                    # Hack required. The Vivado generated hdl files sometimes
                    # have 'sim' in their path, sometimes don't
                    file = None
                    lIpPath = abspath(
                        join(lWorkingDir, 'top.srcs', 'sources_1', 'ip'))

                    # ----------------------------------------------------------
                    for lDir in ['', 'sim']:
                        for lExt in ['vhd', 'v']:
                            lPathToIp = join(
                                lIpPath, lName, lDir, lName + '.' + lExt)
                            if not exists(join(lPathToIp)):
                                continue

                            file = lPathToIp
                            break
                        # File found, stop here
                        if file is not None:
                            break
                    # ----------------------------------------------------------

                    if file is None:
                        raise IOError(
                            'No simulation source found for core \'' + lBasename + '\'')
                    # ----------------------------------------------------------
                else:
                    file = src.FilePath
                # ----------------------------------------------------------

                # ----------------------------------------------------------
                if splitext(file)[1] in ['.vhd', '.vhdl']:
                    if src.Vhdl2008:
                        cmd = 'vcom -2008'
                    else:
                        cmd = 'vcom'
                elif splitext(file)[1] == '.v':
                    cmd = 'vlog'

                elif lMap is not None:
                    continue

                else:
                    print('# IGNORING unknown source file type in Modelsim build: {0}'.format(
                        src.FilePath))
                    continue
                # ----------------------------------------------------------

                if src.Lib:
                    cmd = '{0} -work {1}'.format(cmd, src.Lib)
                # ----------------------------------------------------------

            if self.turbo:
                # In turbo mode group compilation commands together
                if not lSrcCommandGroups or lSrcCommandGroups[-1]['cmd'] != cmd:
                    lSrcCommandGroups.append( {'cmd': cmd, 'files': [file]} )
                else:
                    lSrcCommandGroups[-1]['files'].append(file)

            else:
                # execute them immediately when turbo is disabled instead
                write('{0} {1}'.format(cmd, file))
            # ----------------------------------------------------------

        if self.turbo:
            # for cmd, files in lSrcCommandGroups.iteritems():
            for item in lSrcCommandGroups:
                write('{0} {1}'.format(item['cmd'], ' '.join(item['files'])))
# --------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
