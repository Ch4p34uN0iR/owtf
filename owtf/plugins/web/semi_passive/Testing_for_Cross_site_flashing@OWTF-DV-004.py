"""
Cross Site Flashing semi passive plugin: Tries to retrieve the crossdomain.xml
file and display it for review
"""

from owtf.dependency_management.dependency_resolver import ServiceLocator


DESCRIPTION = "Normal requests for XSF analysis"


def run(PluginInfo):
    url_list = []
    for File in ["crossdomain.xml", "clientaccesspolicy.xml"]:
        for url in ServiceLocator.get_component("target").get_as_list(['target_url', 'top_url']):
            url_list.append(url + "/" + File)  # Compute all URL + File combinations
    # The requester owtf component will unique the URLs
    TransactionList = ServiceLocator.get_component("requester").get_transactions(True, url_list)
    # Even though we have transaction list, those transactions do not have id
    # because our proxy stores the transactions and not the requester. So the
    # best way is to use the url list to retrieve transactions while making the
    # report
    return ServiceLocator.get_component("plugin_helper").TransactionTableForURLList(True, url_list, "GET")
