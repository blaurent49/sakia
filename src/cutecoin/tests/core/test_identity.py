import sys
import unittest
import asyncio
import quamash
import logging
import time
from PyQt5.QtCore import QLocale
from cutecoin.core.registry.identities import Identity, IdentitiesRegistry, LocalState, BlockchainState
from cutecoin.tests.mocks.monkeypatch import pretender_reversed
from cutecoin.tests.mocks.bma import nice_blockchain, corrupted
from cutecoin.tests import get_application
from cutecoin.core import Application, Community
from cutecoin.core.net import Network, Node
from ucoinpy.documents.peer import BMAEndpoint
from cutecoin.core.net.api.bma.access import BmaAccess
from cutecoin.tools.exceptions import MembershipNotFoundError
from ucoinpy.api.bma import API


class TestIdentity(unittest.TestCase):
    def setUp(self):
        self.qapplication = get_application()
        QLocale.setDefault(QLocale("en_GB"))
        self.lp = quamash.QEventLoop(self.qapplication)
        asyncio.set_event_loop(self.lp)
        self.identities_registry = IdentitiesRegistry()

        self.application = Application(self.qapplication, self.lp, self.identities_registry)
        self.application.preferences['notifications'] = False

        self.endpoint = BMAEndpoint("", "127.0.0.1", "", 50000)
        self.node = Node("test_currency", [self.endpoint],
                         "", "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
                         None, Node.ONLINE,
                         time.time(), {}, "ucoin", "0.12.0", 0)
        self.network = Network.create(self.node)
        self.bma_access = BmaAccess.create(self.network)
        self.community = Community("test_currency", self.network, self.bma_access)

    def tearDown(self):
        try:
            self.lp.close()
        finally:
            asyncio.set_event_loop(None)

    def test_identity_membership(self):
        mock = nice_blockchain.get_mock()
        time.sleep(2)
        logging.debug(mock.pretend_url)
        API.reverse_url = pretender_reversed(mock.pretend_url)
        identity = Identity("john", "7Aqw6Efa9EzE7gtsc8SveLLrM7gm6NEGoywSv4FJx6pZ",
                            LocalState.COMPLETED, BlockchainState.VALIDATED)

        @asyncio.coroutine
        def exec_test():
            ms = yield from identity.membership(self.community)
            self.assertEqual(ms["blockNumber"], 0)
            self.assertEqual(ms["blockHash"], "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709")
            self.assertEqual(ms["membership"], "IN")
            self.assertEqual(ms["currency"], "test_currency")

        self.lp.run_until_complete(exec_test())
        mock.delete_mock()

    def test_identity_corrupted_membership(self):
        mock = corrupted.get_mock()
        time.sleep(2)
        logging.debug(mock.pretend_url)
        API.reverse_url = pretender_reversed(mock.pretend_url)
        identity = Identity("john", "7Aqw6Efa9EzE7gtsc8SveLLrM7gm6NEGoywSv4FJx6pZ",
                            LocalState.COMPLETED, BlockchainState.VALIDATED)

        @asyncio.coroutine
        def exec_test():
            with self.assertRaises(MembershipNotFoundError):
                yield from identity.membership(self.community)

        self.lp.run_until_complete(exec_test())
        mock.delete_mock()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
