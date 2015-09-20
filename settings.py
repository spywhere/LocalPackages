import sublime


class Settings:

    """
    Settings collections for easier access and managements
    """

    @staticmethod
    def reset():
        """
        Reset all changes (used on restart)
        """
        Settings.settings = None
        Settings.sublime_settings = None
        Settings.settings_base = "LocalPackages.sublime-settings"
        Settings.sublime_base = "Preferences.sublime-settings"

    @staticmethod
    def startup():
        """
        Read all settings from files
        """
        Settings.settings = sublime.load_settings(Settings.settings_base)
        Settings.sublime_settings = sublime.load_settings(Settings.sublime_base)

    @staticmethod
    def get_global(key, default=None, as_tuple=False):
        """
        Returns a value in default settings file

        @param key: a key to get value
        @param default: a return value if specified key is not exists
        @param as_tuple: if provided as True, will returns as a tuple contains
            value and a boolean specified if value gather from project
            settings or not
        """
        if as_tuple:
            return (Settings.get_global(key, default, as_tuple=False), False)
        else:
            return Settings.settings.get(key, default)

    @staticmethod
    def get_local(key, default=None, as_tuple=False):
        """
        Returns a value in project settings file

        @param key: a key to get value
        @param default: a return value if specified key is not exists
        @param as_tuple: if provided as True, will returns as a tuple contains
            value and a boolean specified if value gather from project
            settings or not
        """
        if as_tuple:
            return (Settings.get_local(key, default, as_tuple=False), True)
        else:
            project_data = sublime.active_window().project_data()
            if (project_data is not None and
                    "local_packages" in project_data and
                    key in project_data["local_packages"]):
                return project_data["local_packages"][key]
        return default

    @staticmethod
    def get_sublime(key, default=None):
        """
        Returns a value in Sublime Text's settings file

        @param key: a key to get value
        @param default: a return value if specified key is not exists
        """
        return Settings.sublime_settings.get(key, default)

    @staticmethod
    def get(key, default=None, from_global=None, as_tuple=False):
        """
        Returns a value in settings

        @param key: a key to get value
        @param default: a return value if specified key is not exists
        @param as_tuple: if provided as True, will returns as a tuple contains
            value and a boolean specified if value gather from project
            settings or not

        This method must return in local-default prioritize order
        """
        if from_global is None:
            value = Settings.get(
                key,
                default=None,
                from_global=False,
                as_tuple=as_tuple
            )
            if value is None:
                value = Settings.get(
                    key,
                    default=default,
                    from_global=True,
                    as_tuple=as_tuple
                )
            return value
        elif from_global:
            return Settings.get_global(key, default, as_tuple)
        else:
            return Settings.get_local(key, default, as_tuple)

    @staticmethod
    def set(key, val, to_global=False):
        """
        Set a value to specified key in settings

        @param key: a key to set value
        @param val: a value to be set, if provided as not None,
            otherwise key will be deleted instead
        @param to_global: if provided as True, will set the value to
            default settings
        """
        if to_global:
            if val is None:
                if Settings.settings.has(key):
                    Settings.settings.erase(key)
                else:
                    # Return here so it won't wasting time saving old settings
                    return
            else:
                Settings.settings.set(key, val)
            sublime.save_settings(Settings.settings_base)
        else:
            window = sublime.active_window()
            project_data = window.project_data()
            if val is None:
                if (project_data is not None and
                        "local_packages" in project_data and
                        key in project_data["local_packages"]):
                    del project_data["local_packages"][key]
                else:
                    # Return here so it won't wasting time saving old settings
                    return
            else:
                if "local_packages" in project_data:
                    data = project_data["local_packages"]
                else:
                    data = {}
                data[key] = val
                project_data["local_packages"] = data
            window.set_project_data(project_data)

    @staticmethod
    def ready():
        """
        Returns whether settings are ready to be used
        """
        return Settings.settings is not None
