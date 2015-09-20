try:
    PackageInstaller = __import__("Package Control").package_control.package_installer.PackageInstaller
    PackageInstallerThread = __import__("Package Control").package_control.package_installer.PackageInstallerThread
    text = __import__("Package Control").package_control.text
    ThreadProgress = __import__("Package Control").package_control.thread_progress.ThreadProgress
    package_control_installed = True
except:
    package_control_installed = False

import sublime
import threading


class PackagesInstallerThread(threading.Thread, PackageInstaller):

    """
    A thread to run the action of retrieving available packages in. Uses the
    default PackageInstaller.on_done quick panel handler.
    """

    def __init__(self, window, missing_packages, callback=None):
        """
        :param window:
            An instance of :class:`sublime.Window` that represents the Sublime
            Text window to show the available package list in.
        """

        self.window = window
        self.completion_type = 'installed'
        self.missing_packages = missing_packages
        self.callback = callback
        threading.Thread.__init__(self)
        PackageInstaller.__init__(self)

    def run(self):
        if not package_control_installed:
            print("[Local Packages] Error while trying to install packages")
            return
        print("[Local Packages] Installing %s missing packages" % (
            len(self.missing_packages)
        ))
        self.package_list = self.make_package_list(
            ['upgrade', 'downgrade', 'reinstall', 'pull', 'none']
        )

        def install():
            if not self.package_list:
                sublime.message_dialog(text.format(
                    u'''
                    Local Packages
                    There are no packages available for installation
                    '''
                ))
                return
            self.available_packages = [p[0] for p in self.package_list]
            self.failed_packages = []
            self.install_packages()

        sublime.set_timeout(install, 10)

    def install_packages(self):
        if len(self.missing_packages) <= 0:
            if self.callback:
                self.callback(self.failed_packages)
        missing_package = self.missing_packages[0]
        self.missing_packages = self.missing_packages[1:]
        if missing_package in self.available_packages:
            self.install_package(missing_package)
        else:
            self.failed_packages.append(missing_package)

    def install_package(self, name):
        """
        Quick panel user selection handler - disables a package, installs or
        upgrades it, then re-enables the package
        :param picked:
            An integer of the 0-based package name index from the presented
            list. -1 means the user cancelled.
        """

        if name in self.disable_packages(name, 'install'):
            def on_complete():
                self.reenable_package(name, 'install')
                self.install_packages()
        else:
            def on_complete():
                self.install_packages()

        thread = PackageInstallerThread(self.manager, name, on_complete)
        thread.start()
        ThreadProgress(
            thread,
            'Installing package %s' % name,
            'Package %s successfully %s' % (name, self.completion_type)
        )
