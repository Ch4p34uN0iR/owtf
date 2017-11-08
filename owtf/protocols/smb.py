"""
owtf.protocols.smb
~~~~~~~~~~~~~~~~~~

Description:
This is the handler for the Social Engineering Toolkit (SET) trying to overcome
the limitations of set-automate.
"""

from owtf.shell import pexpect_shell
from owtf.lib.general import *
from owtf.utils import FileOperations


class SMB(pexpect_shell.PExpectShell):

    COMPONENT_NAME = "smb"

    def __init__(self):
        self.register_in_service_locator()
        # Calling parent class to do its init part.
        pexpect_shell.PExpectShell.__init__(self)
        self.command_time_offset = 'SMBCommand'
        self.mounted = False

    def is_mounted(self):
        return self.mounted

    def set_mounted(self, value):
        self.mounted = value

    def check_mount_point_existence(self, options):
        if not os.path.exists(options['SMB_MOUNT_POINT']):
            FileOperations.make_dirs(options['SMB_MOUNT_POINT'])

    def mount(self, options, plugin_info):
        if self.is_mounted():
            return True
        cprint("Initialising shell..")
        self.Open(options, plugin_info)
        cprint("Ensuring Mount Point %s exists..." % options['SMB_MOUNT_POINT'])
        self.check_mount_point_existence(options)
        mount_cmd = "smbmount //%s/%s %s" % (options['SMB_HOST'], options['SMB_SHARE'], options['SMB_MOUNT_POINT'])
        if options['SMB_USER']:  # Pass user if specified.
            mount_cmd += " -o user=%s" % options['SMB_USER']
        cprint("Mounting share..")
        self.run(mount_cmd, plugin_info)
        self.expect("Password:")
        if options['SMB_PASS']:  # Pass password if specified.
            self.run(options['SMB_PASS'], plugin_info)
        else:
            self.run("", plugin_info)  # Send blank line.
        self.expect("#")
        self.set_mounted(True)

    def transfer(self):
        operation = False
        if self.options['SMB_DOWNLOAD']:
            self.download("%s/%s" % (self.options['SMB_MOUNT_POINT'], self.options['SMB_DOWNLOAD']), ".")
            operation = True
        if self.options['SMB_UPLOAD']:
            self.upload(
                self.options['SMB_UPLOAD'],
                self.options['SMB_MOUNT_POINT'])
            operation = True
        if not operation:
            cprint("Nothing to do: no SMB_DOWNLOAD or SMB_UPLOAD specified..")

    def unmount(self, plugin_info):
        if self.is_mounted():
            self.shell_exec_monitor("umount %s" % self.options['SMB_MOUNT_POINT'])
            self.set_mounted(False)
            self.close(plugin_info)

    def upload(self, file_path, mount_point):
        cprint("Copying %s to %s" % (file_path, mount_point))
        self.shell_exec_monitor("cp -r %s %s" % (file_path, mount_point))

    def download(self, remote_file_path, target_dir):
        cprint("Copying %s to %s" % (remote_file_path, target_dir))
        self.shell_exec_monitor("cp -r %s %s" % (remote_file_path, target_dir))
