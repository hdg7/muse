import importlib
import os
import sys

from muse.utils.env import get_plugins_dir


def _importer_handler(path: str, base_class: type, plugin_folder: str):
    for importer_file in os.listdir(path):
        if importer_file.endswith(".py"):
            spec = importlib.util.spec_from_file_location(
                f"muse.plugins.{plugin_folder}.{importer_file[:-3]}",
                os.path.join(path, importer_file),
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[f"muse.plugins.{plugin_folder}.{importer_file[:-3]}"] = module

            for name, obj in module.__dict__.items():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, base_class)
                    and obj != base_class
                ):
                    obj.plugin = True


def import_from_plugin(plugin_folder: str, base_class: type, *alternative_folders: str):
    """
    Import all the importers from the plugins directory.

    :param plugin_folder: The folder where the importers are stored.
    :param base_class: The base class of the importers.
    :param alternative_folders: Alternative folders where the importers are stored.
    """

    plugins_dir = get_plugins_dir()
    if os.path.exists(plugins_dir):
        for folder in plugin_folder, *alternative_folders:
            if os.path.exists(os.path.join(plugins_dir, folder)):
                _importer_handler(os.path.join(plugins_dir, folder), base_class, folder)
