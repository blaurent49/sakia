'''
Created on 2 févr. 2014

@author: inso
'''
import logging
from math import pow

from PyQt5.QtWidgets import QDialog,QFrame, QSlider, QLabel, QDialogButtonBox, QErrorMessage
from PyQt5.QtCore import Qt, QSignalMapper


from cutecoin.models.coin import Coin
from cutecoin.models.person import Person
from cutecoin.models.node import Node
from cutecoin.models.coin.listModel import CoinsListModel

from cutecoin.gen_resources.transferDialog_uic import Ui_TransferMoneyDialog

class TransferMoneyDialog(QDialog, Ui_TransferMoneyDialog):
    '''
    classdocs
    '''
    def __init__(self, sender):
        '''
        Constructor
        '''
        super(TransferMoneyDialog, self).__init__()
        self.setupUi(self)
        self.sender = sender
        for wallet in sender.wallets.walletsList:
            self.comboBox_wallets.addItem(wallet.getText())

        for contact in sender.contacts:
            self.comboBox_contact.addItem(contact.name)

        self.refreshTransaction(sender.wallets.walletsList[0])


    def removeCoinsFromTransfer(self):
        selection = self.listView_coinsSent.selectedIndexes()
        walletCoins = self.listView_wallet.model().coins
        sentCoins = self.listView_coinsSent.model().coins
        newWallet = sentCoins
        for selected in selection:
            coin = sentCoins[selected.row()]
            sentCoins.remove(coin)
            walletCoins.append(coin)
        self.listView_wallet.setModel(CoinsListModel(walletCoins))
        self.listView_coinsSent.setModel(CoinsListModel(newWallet))

    def addCoinsToTransfer(self):
        selection = self.listView_wallet.selectedIndexes()
        walletCoins = self.listView_wallet.model().coins
        sentCoins = self.listView_coinsSent.model().coins
        newWallet = walletCoins
        for selected in selection:
            coin = walletCoins[selected.row()]
            newWallet.remove(coin)
            sentCoins.append(coin)
        self.listView_wallet.setModel(CoinsListModel(newWallet))
        self.listView_coinsSent.setModel(CoinsListModel(sentCoins))

    def openManageWalletCoins(self):
        pass

    def accept(self):
        sentCoins = self.listView_coinsSent.model().toList()
        recipient = None

        if self.radio_keyFingerprint.isChecked():
            recipient = Person("", self.edit_keyFingerprint.text(), "")
        else:
            recipient = self.sender.contacts[self.comboBox_contact.currentIndex()]

        if self.radio_nodeAddress.isChecked():
            node = Node(self.edit_nodeAddress.text(), int(self.edit_port.text()))
        else:
            #TODO: Manage trusted nodes
            node = Node(self.edit_nodeAddress.text(), int(self.edit_port.text()))

        message = self.edit_message.text()
        #TODO: Transfer money, and validate the window if no error happened
        if self.sender.transferCoins(node, recipient, sentCoins, message):
            self.close()
        else:
            QErrorMessage(self).showMessage("Cannot transfer coins.")

    def changeDisplayedWallet(self, index):
        wallet = self.sender.wallets.walletsList[index]
        self.refreshTransaction(wallet)

    def refreshTransaction(self, wallet):
        coinsSentModel = CoinsListModel([])
        self.listView_coinsSent.setModel(coinsSentModel)
        walletCoinsModel = CoinsListModel(list(wallet.coins))
        self.listView_wallet.setModel(walletCoinsModel)

    def recipientModeChanged(self, fingerprintToggled):
        self.edit_keyFingerprint.setEnabled(fingerprintToggled)
        self.comboBox_contact.setEnabled(not fingerprintToggled)

    def transferModeChanged(self, nodeAddressToggled):
        self.edit_nodeAddress.setEnabled(nodeAddressToggled)
        self.comboBox_trustedNode.setEnabled(not nodeAddressToggled)





