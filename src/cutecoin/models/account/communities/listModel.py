'''
Created on 5 févr. 2014

@author: inso
'''

from PyQt5.QtCore import QAbstractListModel, Qt

class CommunitiesListModel(QAbstractListModel):
    '''
    A Qt abstract item model to display communities in a tree
    '''
    def __init__(self, communities, parent=None):
        '''
        Constructor
        '''
        super(CommunitiesListModel, self).__init__(parent)
        self.communities = communities


    def rowCount(self ,parent):
        return len(self.communities.communitiesList)

    def data(self,index,role):

        if role == Qt.DisplayRole:
            row=index.row()
            value = self.communities.communitiesList[row].currency
            return value

    def flags(self,index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
