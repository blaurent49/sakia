'''
Created on 2 févr. 2014

@author: inso
'''
from cutecoin.gen_resources.addCommunityDialog_uic import Ui_AddCommunityDialog
from PyQt5.QtWidgets import QDialog
from cutecoin.models.community.treeModel import CommunityTreeModel
from cutecoin.models.node import MainNode

class AddCommunityDialog(QDialog, Ui_AddCommunityDialog):
    '''
    classdocs
    '''


    def __init__(self, accountDialog):
        '''
        Constructor
        '''
        super(AddCommunityDialog, self).__init__()
        self.setupUi(self)
        self.accountDialog = accountDialog
        self.buttonBox.accepted.connect(self.accountDialog.validAddCommunityDialog)

    def setCommunities(self, communities):
        self.communities = communities

    def addCommunity(self):
        '''
        Add community slot
        '''
        server = self.serverEdit.text()
        port = self.portBox.value()
        community = self.communities.addCommunity(MainNode(server, port))
        self.communityView.setModel( CommunityTreeModel(community) )


