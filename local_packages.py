import sublime
from .package_evaluator import PackageEvaluatorThread
from .event_handler import EventHandler
from .settings import Settings

package_control_installed = False
LOCAL_PACKAGES_VERSION = "0.1.0"
evaluating = False


def plugin_loaded():
    Settings.reset()
    Settings.startup()
    EventHandler().register_handler(
        evaluate_install,
        EventHandler().ON_LOAD
    )
    print("[Local Packages] v%s" % (LOCAL_PACKAGES_VERSION))
    try:
        __import__("Package Control")
        global package_control_installed
        package_control_installed = True
    except:
        sublime.error_message(
            "Package Control is not found.\n\n" +
            "Local Packages will now disabled"
        )
        return
    evaluate_install()


def evaluate_install(view=None):
    global evaluating
    if evaluating:
        return
    print("[Local Packages] Evaluating missing packages")
    evaluating = True
    PackageEvaluatorThread(
        window=sublime.active_window(),
        callback=on_installed
    ).start()


def on_installed(failed_packages=[]):
    global evaluating
    evaluating = False
    if len(failed_packages) > 0:
        msg = "Local Packages failed to install %s missing packages...\n" % (
            len(failed_packages)
        )
        limit = 10
        for package in failed_packages:
            limit -= 1
            if limit < 0:
                break
            msg += "  - %s\n" % (package)
        if limit < 0:
            msg += "and more..."
        sublime.error_message(msg)
    else:
        print("[Local Packages] Dependencies already installed")
