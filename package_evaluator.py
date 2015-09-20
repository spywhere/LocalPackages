try:
    ExistingPackagesCommand = __import__("Package Control").package_control.commands.existing_packages_command.ExistingPackagesCommand
    text = __import__("Package Control").package_control.text
    PackageManager = __import__("Package Control").package_control.package_manager.PackageManager
    package_control_installed = True
except:
    package_control_installed = False

from .package_installer import PackagesInstallerThread
import sublime
import threading
import os
from .settings import Settings


class PackageEvaluatorThread(threading.Thread, ExistingPackagesCommand):
    def __init__(self, window, filter_function=None, callback=None):
        self.window = window
        self.filter_function = filter_function
        self.manager = PackageManager()
        self.callback = callback
        threading.Thread.__init__(self)

    def show_items(self):
        self.package_items = [
            [
                "[-] " + p[0] if (
                    p[0] in self.package_selection and
                    self.package_selection[p[0]]
                ) else "[+] " + p[0],
                p[1],
                "Select to remove from selection" if (
                    p[0] in self.package_selection and
                    self.package_selection[p[0]]
                ) else "Select to add to selection"
            ]
            for p in self.package_list
        ]
        self.window.show_quick_panel(
            self.package_items, self.on_done, 0, self.last_index
        )

    def load_file(self):
        self.package_selection = {}
        dependency_path = None
        for folder in self.window.folders():
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if (os.path.isfile(file_path) and
                        file_name.endswith(".sublime-local-dependency")):
                    dependency_path = file_path
                    break
        dependencies = None
        if dependency_path:
            dep_file = open(dependency_path, "r")
            try:
                dependencies = sublime.decode_value(dep_file.read())
            except:
                pass
            dep_file.close()
        if dependencies and "packages" in dependencies:
            for package_name in dependencies["packages"]:
                self.package_selection[package_name] = True

    def install_missing(self):
        installed_packages = [p[0] for p in self.package_list]
        missing_packages = []
        for package in self.package_selection:
            if package not in installed_packages:
                missing_packages.append(package)
        if len(missing_packages) > 0:
            PackagesInstallerThread(
                self.window, missing_packages, self.callback
            ).start()
        else:
            self.callback(missing_packages)

    def run(self):
        if not package_control_installed:
            print("[Local Packages] Error while trying to evaluate packages")
            return
        if not Settings().get("enabled"):
            print("[Local Packages] Local Packages is disabled on this project")
            return
        self.package_list = self.make_package_list()
        if self.filter_function:
            self.package_list = list(filter(self.filter_function, self.package_list))

        def install():
            if not self.package_list:
                sublime.message_dialog(text.format(
                    u'''
                    Local Packages
                    There are no packages to select
                    '''
                ))
                return
            self.load_file()
            self.install_missing()

        sublime.set_timeout(install, 10)
