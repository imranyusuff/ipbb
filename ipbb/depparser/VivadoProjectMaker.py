from __future__ import print_function
import time
import os


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class VivadoProjectMaker(object):
    # --------------------------------------------------------------
    def __init__(self, aReverse = False):
    # def __init__(self, aPathmaker):
        # self.pathmaker = aPathmaker
        self.reverse = aReverse
        self.FileSets = {
            '.xdc': 'constrs_1',
            '.tcl': 'constrs_1',
            '.mif': 'sources_1',
            '.vhd': 'sources_1',
            '.v': 'sources_1',
            '.xci': 'sources_1',
            '.ngc': 'sources_1',
            '.ucf': 'ise_1',
            '.xco': 'ise_1',
            '.edn': 'sources_1',
            '.edf': 'sources_1'
        }
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    def write(self, aTarget, aScriptVariables, aComponentPaths, aCommandList, aLibs, aMaps):

        if 'device_name' not in aScriptVariables:
            raise RuntimeError("Variable 'device_name' not defined in dep files.")

        # ----------------------------------------------------------
        # FIXME: Tempourary assignments
        write = aTarget
        lWorkingDir = os.path.abspath(os.path.join(os.getcwd(), 'top'))
        # ----------------------------------------------------------

        write('# Autogenerated project build script')
        write(time.strftime("# %c"))
        write()

        write('set outputDir {0}'.format(lWorkingDir))
        write('file mkdir $outputDir')

        write(
            'create_project top $outputDir -part {device_name}{device_package}{device_speed} -force'.format(
                **aScriptVariables
            )
        )

        write(
            'if {[string equal [get_filesets -quiet constrs_1] ""]} {create_fileset -constrset constrs_1}')
        write(
            'if {[string equal [get_filesets -quiet sources_1] ""]} {create_fileset -srcset sources_1}')
        write(
            'if {[string equal [get_filesets -quiet ise_1] ""]} {create_fileset -srcset ise_1}')

        for setup in aCommandList['setup']:
            write('source {0}'.format(setup.FilePath))

        lXciBasenames = []
        lXciTargetFiles = []

        lSrcs = aCommandList['src'] if not self.reverse else reversed(aCommandList['src'])

        for src in lSrcs:
            lPath, lBasename = os.path.split(src.FilePath)
            lName, lExt = os.path.splitext(lBasename)
            lTargetFile = os.path.join(
                '$outputDir/top.srcs/sources_1/ip', lName, lBasename)

            if lExt == '.xci':
                write(
                    'import_files -norecurse -fileset sources_1 {0}'.format(src.FilePath))
                lXciBasenames.append(lName)
                lXciTargetFiles.append(lTargetFile)
            else:
                if src.Include:
                    cmd = 'add_files -norecurse -fileset {1} {0}'.format(
                        src.FilePath, self.FileSets[lExt])
                    if src.Vhdl2008:
                        cmd += '\nset_property FILE_TYPE {{VHDL 2008}} [get_files {0}]'.format(
                            src.FilePath)
                    if lExt == '.tcl':
                        write(
                            'set_property USED_IN implementation [' + cmd + ']')
                    else:
                        write(cmd)
                if src.Lib:
                    write('set_property library {1} [ get_files [ {0} ] ]'.format(
                        src.FilePath, src.Lib))

        write('set_property top top [current_fileset]')

        write(
            'set_property "steps.synth_design.args.flatten_hierarchy" "none" [get_runs synth_1]')

        for i in lXciBasenames:
            write('upgrade_ip [get_ips {0}]'.format(i))
        for i in lXciTargetFiles:
            write('create_ip_run [get_files {0}]'.format(i))
        write('close_project')
    # --------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
