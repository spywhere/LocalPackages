import sublime
from .event_handler import EventHandler
from .settings import Settings

package_control_installed = False
LOCAL_PACKAGES_VERSION = "0.1.3"
evaluating = False
already_evaluate = False
retry_times = 3


def plugin_loaded():
    Settings.reset()
    Settings.startup()
    print("[Local Packages] v%s" % (LOCAL_PACKAGES_VERSION))
    check_package_control()


def check_package_control():
    try:
        __import__("Package Control").package_control
        global package_control_installed
        package_control_installed = True
    except:
        global retry_times
        if retry_times > 0:
            retry_times -= 1
            sublime.set_timeout(check_package_control, 3000)
        else:
            sublime.error_message(
                "Package Control is not found.\n\n" +
                "Local Packages will now disabled"
            )
        return
    EventHandler().register_handler(
        evaluate_install,
        EventHandler().ON_LOAD
    )
    evaluate_install()


def evaluate_install(view=None):
    global evaluating, already_evaluate
    if evaluating:
        return
    if not already_evaluate:
        print("[Local Packages] Evaluating missing packages")
    from .package_evaluator import PackageEvaluatorThread
    evaluating = True
    PackageEvaluatorThread(
        window=sublime.active_window(),
        callback=on_installed
    ).start()


def on_installed(failed_packages=[]):
    global evaluating, already_evaluate
    evaluating = False
    if already_evaluate:
        return
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
    already_evaluate = True
