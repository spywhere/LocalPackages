try:
    ExistingPackagesCommand = __import__("Package Control").package_control.commands.existing_packages_command.ExistingPackagesCommand
    text = __import__("Package Control").package_control.text
    PackageManager = __import__("Package Control").package_control.package_manager.PackageManager
    package_control_installed = True
except:
    package_control_installed = False

import sublime
import sublime_plugin
import threading
import os


class LocalPackagesCreateCommand(sublime_plugin.WindowCommand):
    def run(self):
        if package_control_installed:
            PackageSelectionThread(self.window).start()


class PackageSelectionThread(threading.Thread, ExistingPackagesCommand):
    def __init__(self, window, filter_function=None):
        self.window = window
        self.filter_function = filter_function
        self.manager = PackageManager()
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

    def generate_file(self):
        if len(self.window.folders()) <= 0:
            sublime.error_message(
                "No folder opened. Local dependency creation cancelled."
            )
            return
        dep_file = open(os.path.join(
            self.window.folders()[0],
            os.path.basename(self.window.folders()[0]) + ".sublime-local-dependency"
        ), "w")
        dependencies = {
            "packages": []
        }
        for package in self.package_selection:
            dependencies["packages"].append(package)
        dep_file.write(sublime.encode_value(dependencies, True))
        dep_file.close()

    def run(self):
        self.package_list = self.make_package_list()
        if self.filter_function:
            self.package_list = list(filter(self.filter_function, self.package_list))

        def show_panel():
            if not self.package_list:
                sublime.message_dialog(text.format(
                    u'''
                    Local Packages
                    There are no packages to select
                    '''
                ))
                return
            self.last_index = 0
            self.load_file()
            self.show_items()

        sublime.set_timeout(show_panel, 10)

    def on_done(self, picked):
        if picked == -1:
            self.generate_file()
            return
        self.last_index = picked
        package_name = self.package_list[picked][0]
        if (package_name in self.package_selection and
                self.package_selection[package_name]):
            self.package_selection[package_name] = False
        else:
            self.package_selection[package_name] = True
        self.show_items()
