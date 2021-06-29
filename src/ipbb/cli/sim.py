
# Modules
import click

# from ..cmds import sim

# kIPExportDir = 'ipcores_sim'
import types

from os.path import join


# ------------------------------------------------------------------------------
@click.group('sim', short_help="Set up simulation projects.", chain=True)
@click.pass_obj
@click.option('-p', '--proj', metavar='<name>', default=None, help='Switch to <name> before running subcommands.')
def sim(env, proj):
    '''Simulation commands group'''
    # from ..cmds.sim import sim
    # sim(env, proj)
    pass

# ------------------------------------------------------------------------------
@sim.resultcallback()
@click.pass_obj
def process_sim(env, subcommands, proj):

    from ..cmds.sim import sim
    sim(env, proj)

    # Executed the chained commands
    for name, cmd, args, kwargs in subcommands:
        cmd(*args, **kwargs)


# ------------------------------------------------------------------------------
def sim_get_command_aliases(self, ctx, cmd_name):
    """
    Temporary hack for backward compatibility
    """
    rv = click.Group.get_command(self, ctx, cmd_name)
    if rv is not None:
        return rv

sim.get_command = types.MethodType(sim_get_command_aliases, sim)
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
@sim.command('setup-simlib', short_help="Compile xilinx simulation libraries")
@click.option('-x', '--xilinx-simlib', 'aXilSimLibsPath', default=join('${HOME}', '.xilinx_sim_libs'), envvar='IPBB_SIMLIB_BASE', metavar='<path>', help='Xilinx simulation library target directory. The default value is overridden by IPBB_SIMLIB_BASE environment variable when defined', show_default=True)
@click.option('-f', '--force', 'aForce', is_flag=True, help="Force simlib compilation/check.")
@click.pass_obj
@click.pass_context
def setupsimlib(ctx, *args, **kwargs):
    """Generate the Vivado simulation libraries for the current simulator (modelsim, questasim)
    """
    from ..cmds.sim import setupsimlib
    return (ctx.command.name, setupsimlib, args, kwargs)

# ------------------------------------------------------------------------------
@sim.command('ipcores', short_help="Generate vivado sim cores for the current design.")
@click.option('-x', '--xilinx-simlib', 'aXilSimLibsPath', default=join('${HOME}', '.xilinx_sim_libs'), envvar='IPBB_SIMLIB_BASE', metavar='<path>', help='Xilinx simulation library target directory. The default value is overridden by IPBB_SIMLIB_BASE environment variable when defined', show_default=True)
@click.option('-s', '--to-script', 'aToScript', default=None, help="Write Vivado tcl script to file and exit (dry run).")
@click.option('-o', '--to-stdout', 'aToStdout', is_flag=True, help="Print Vivado tcl commands to screen (dry run).")
@click.pass_obj
@click.pass_context
def ipcores(ctx, *args, **kwargs):
    '''
    Generate the vivado libraries and cores required to simulate the current design.

    '''
    from ..cmds.sim import ipcores
    return (ctx.command.name, ipcores, args, kwargs)


# ------------------------------------------------------------------------------
@sim.command('fli-eth')
@click.option('-d', '--dev', metavar='DEVICE', default='tap0', help='Virtual network device')
@click.option('-i', '--ipbuspkg', metavar='IPBUSPACKAGE', default='ipbus-firmware', help='ipbus firmware package')
@click.pass_obj
@click.pass_context
def fli_eth(ctx, *args, **kwargs):
    """
    Build the Modelsim-ipbus foreign language interface
    """
    from ..cmds.sim import fli_eth
    return (ctx.command.name, fli_eth, args, kwargs)

# ------------------------------------------------------------------------------
@sim.command('ghdl-vhpidirect-eth')
@click.option('-d', '--dev', metavar='DEVICE', default='tap0', help='Virtual network device')
@click.option('-i', '--ipbuspkg', metavar='IPBUSPACKAGE', default='ipbus-firmware', help='ipbus firmware package')
@click.pass_obj
@click.pass_context
def vhpidirect_eth(ctx, *args, **kwargs):
    """
    Build the GHDL-ipbus foreign language interface
    """
    from ..cmds.sim import vhpidirect_eth
    return (ctx.command.name, vhpidirect_eth, args, kwargs)

# ------------------------------------------------------------------------------
@sim.command('fli-udp')
@click.option('-p', '--port', metavar='PORT', default='50001', help='UPD interface port')
@click.option('-i', '--ipbuspkg', metavar='IPBUSPACKAGE', default='ipbus-firmware', help='ipbus firmware package')
@click.pass_obj
@click.pass_context
def fli_udp(ctx, *args, **kwargs):
    """
    Build the Modelsim-ipbus foreign language interface
    """
    from ..cmds.sim import fli_udp
    return (ctx.command.name, fli_udp, args, kwargs)


# ------------------------------------------------------------------------------
@sim.command('ghdl-vhpidirect-udp')
@click.option('-p', '--port', metavar='PORT', default='50001', help='UPD interface port')
@click.option('-i', '--ipbuspkg', metavar='IPBUSPACKAGE', default='ipbus-firmware', help='ipbus firmware package')
@click.pass_obj
@click.pass_context
def vhpidirect_udp(ctx, *args, **kwargs):
    """
    Build the GHDL-ipbus foreign language interface
    """
    from ..cmds.sim import vhpidirect_udp
    return (ctx.command.name, vhpidirect_udp, args, kwargs)


# ------------------------------------------------------------------------------
@sim.command('generate-project', short_help="Assemble the simulation project from sources")
@click.option(' /-1', '--opt/--no-opt', 'aOptimise', default=True, help="Disable project creation optimization. If present sources are added one at a time.")
@click.option('-s', '--to-script', 'aToScript', default=None, help="Write Modelsim tcl script to file and exit (dry run).")
@click.option('-o', '--to-stdout', 'aToStdout', is_flag=True, help="Print Modelsim tcl commands to screen and exit (dry run).")
@click.option('-t', '--simtype', 'aSimType', default=None, help="Specify which sim to use.")
@click.option('-y', '--use-synopsys', 'aUseSynopsys', is_flag=True, help="For GHDL, use non-standard synopsys library.")
@click.pass_obj
@click.pass_context
def genproject(ctx, *args, **kwargs):
    """
    Creates the modelsim project

    \b
    1. Compiles the source code into the 'work' simulation library. A different name can be specified with the `sim.library` dep file setting.
    2. Generates a 'run_sim' wrapper that sets the simulation environment before invoking vsim. The list of desing units to run can be specified with the `sim.run_sim.desing_units` dep file setting.

    NOTE: The ip/mac address of ipbus desings implementing a fli and exposing the ip/mac addresses via  top level generics can be set by defining the following user settings:

    \b
    - 'ipbus.fli.mac_address': mapped to MAC_ADDR top-level generic
    - 'ipbus.fli.ip_address': mapped to IP_ADDR top-level generic

    """
    from ..cmds.sim import genproject
    return (ctx.command.name, genproject, args, kwargs)

# ------------------------------------------------------------------------------
@sim.command()
@click.option('--dev', metavar='DEVICE', default='tap0', help='name of the new device')
@click.option('--ip', metavar='IP', default='192.168.201.1', help='ip address of the virtual interface')
@click.pass_obj
@click.pass_context
def virtualtap(ctx, *args, **kwargs):
    """VirtualTap
    """
    from ..cmds.sim import virtualtap
    return (ctx.command.name, virtualtap, args, kwargs)


# ------------------------------------------------------------------------------
@sim.command('mifs')
@click.pass_obj
@click.pass_context
def mifs(ctx, *args, **kwargs):
    """Import MIF files from project
    """
    from ..cmds.sim import mifs
    return (ctx.command.name, mifs, args, kwargs)


# ------------------------------------------------------------------------------
@sim.command('validate-settings', short_help='Validate project settings.')
@click.pass_obj
@click.pass_context
def validate_settings(ictx, *args, **kwargs):
    '''Make the Vivado project from sources described by dependency files.'''
    from ..cmds.sim import validate_settings
    return (ictx.command.name, validate_settings, args, kwargs)
