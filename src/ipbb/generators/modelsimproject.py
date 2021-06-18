import time
import os

from os.path import join, split, exists, splitext, abspath
from ..utils import SmartOpen

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class ModelSimGenerator(object):
    # --------------------------------------------------------------
    def __init__(self, aProjInfo, aSimLibrary, aIPProjName, aTurbo=True):
        self.projInfo = aProjInfo
        self.simLibrary = aSimLibrary
        self.ipProjName = aIPProjName
        self.turbo = aTurbo

    # --------------------------------------------------------------
    def write(self, aTarget, aSettings, aComponentPaths, aCommandList, aLibs):

        # ----------------------------------------------------------
        # FIXME: Temp assignments
        write = aTarget
        lIPProjDir = abspath(join(self.projInfo.path, self.ipProjName))
        # ----------------------------------------------------------

        # ----------------------------------------------------------
        write('# Autogenerated project build script')
        write(time.strftime('# %c'))
        write()
        write('onerror { quit -code 255 }')

        for setup in (c for c in aCommandList['setup'] if not c.finalize):
            write('source {0}'.format(setup.filepath))

        write(f'vlib {self.simLibrary}')

        for lib in set(aLibs):
            write(f'vlib {lib}')
            write(f'vmap {lib} {lib}')

        lSrcs = aCommandList['src']

        lSrcCommandGroups = []
        # ----------------------------------------------------------
        for src in lSrcs:

            lPath, lBasename = split(src.filepath)
            lName, lExt = splitext(lBasename)

            # ----------------------------------------------------------
            if lExt == '.xco':
                file = abspath(join(lPath, lName + '.vhd'))
            elif lExt in ('.xci', '.xcix'):
                # Hack required. The Vivado generated hdl files sometimes
                # have 'sim' in their path, sometimes don't
                file = None
                lIpPath = abspath(
                    join(lIPProjDir, self.ipProjName + '.srcs', 'sources_1', 'ip'))

                # ----------------------------------------------------------
                # TOFIX: Duplicate of cmds.sim.detect_ip_sim_srcs
                for lGenDir in ['src', 'gen']:
                    for lSimDir in ['', 'sim']:
                        for lExt in ['vhd', 'v']:
                            lPathToIp = abspath(join(
                                lIPProjDir, f'{self.ipProjName}.{lGenDir}', 'sources_1', 'ip', lName, lSimDir, f'{lName}.{lExt}'))
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

                # And stop here w/o including the file to the source list.
                # Because it's already been compiled in the ipcores modelsim libraries by vivado.
                continue
            else:
                file = src.filepath
            # ----------------------------------------------------------

            # ----------------------------------------------------------
            if splitext(file)[1] in ['.vhd', '.vhdl']:
                if src.vhdl2008:
                    cmd = 'vcom -2008'
                else:
                    cmd = 'vcom'
            elif splitext(file)[1] == '.v':
                cmd = 'vlog'

            else:
                print(f'# IGNORING unknown source file type in Modelsim build: {src.filepath}')
                continue

            # ----------------------------------------------------------

            if src.simflags:
                cmd = f'{cmd} {src.simflags}'
            # ----------------------------------------------------------

            lib = src.lib if src.lib else self.simLibrary
            cmd = f'{cmd} -work {lib}'
            # ----------------------------------------------------------

            if self.turbo:
                # In turbo mode group compilation commands together
                if not lSrcCommandGroups or lSrcCommandGroups[-1]['cmd'] != cmd:
                    lSrcCommandGroups.append( {'cmd': cmd, 'files': [file]} )
                else:
                    lSrcCommandGroups[-1]['files'].append(file)

            else:
                # execute them immediately when turbo is disabled instead
                write(f'{cmd} {file}')
            # ----------------------------------------------------------

        if self.turbo:
            # for cmd, files in lSrcCommandGroups.items():
            for item in lSrcCommandGroups:
                write(f'{item["cmd"]} {" ".join(item["files"])}')

        for setup in (c for c in aCommandList['setup'] if c.finalize):
            write(f'source {setup.filepath}')

# --------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
