## Local Packages

A Sublime Text's local packages installer

[![Release](https://img.shields.io/github/release/spywhere/LocalPackages.svg?style=flat)](https://github.com/spywhere/LocalPackages/releases)
[![Issues](https://img.shields.io/github/issues/spywhere/LocalPackages.svg?style=flat)](https://github.com/spywhere/LocalPackages/issues)
[![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/spywhere/LocalPackages/blob/master/LICENSE)

### What is Local Packages
Local Packages is a plugin to allows Package Control's users easily install the missing Sublime Text's packages based on the project.

Local Packages is just a `Package Control` extension plugin **not** `Package Control` replacement.

### How it works?
When open the project, Local Packages will seach for `.sublime-local-dependency` file in the project and evaluate if the package list already contains the dependencies. If any missing dependency is found, Local Packages will automatically install for you.

The installation process is depends on `Package Control` installation. Any `Package Control` settings will be used while installing the missing packages.

### How to use it?
Just open the Command Palette and type `Create Local Dependencies`, select the packages and `.sublime-local-dependency` file will be created for you.

### Settings
Local Packages is using a very complex settings system in which you can control how settings affect the whole Sublime Text or each project you want.

As you might already know, you can override default settings by set the desire settings inside user's settings file (can be access via `Preferences > Packages Settings > Local Packages > Settings - User`).

But if you want to override the settings for particular project, you can add the `local_packages` dictionary to the .sublime-project file. Under this dictionary, it works like a user's settings file but for that project instead.

To summarize, Local Packages will look for any settings in your project settings file first, then user's settings file, and finally, the default package settings.
