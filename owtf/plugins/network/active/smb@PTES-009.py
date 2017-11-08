"""
Plugin for probing SMB
"""

from owtf.dependency_management.dependency_resolver import ServiceLocator


DESCRIPTION = " SMB Probing "


def run(PluginInfo):
    resource = ServiceLocator.get_component("resource").get_resources('SmbProbeMethods')
    return ServiceLocator.get_component("plugin_helper").CommandDump('Test Command', 'Output', resource, PluginInfo, [])
