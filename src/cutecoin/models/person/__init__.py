'''
Created on 11 févr. 2014

@author: inso
'''

import ucoinpy as ucoin
from cutecoin.core.exceptions import PersonNotFoundError

class Person(object):
    '''
    A person with a name, a fingerprint and an email
    Created by the person.factory
    '''


    def __init__(self, name, fingerprint, email):
        '''
        Constructor
        '''
        self.name = name
        self.fingerprint = fingerprint
        self.email = email


    @classmethod
    def lookup(cls, fingerprint, community):
        '''
        Create a person from the fngerprint found in a community
        '''
        keys = community.ucoinRequest(ucoin.pks.Lookup(),
                                          get_args={'search':"0x"+fingerprint, 'op':'index'})['keys']
        if len(keys) > 0:
            json = keys[0]['key']
            name = json['name']
            fingerprint = json['fingerprint']
            email = json['email']
            return cls(name, fingerprint, email)
        else:
            raise PersonNotFoundError(fingerprint, "fingerprint", community)
        return None

    @classmethod
    def fromJson(cls, jsonPerson):
        '''
        Create a person from json data
        '''
        name = jsonPerson['name']
        fingerprint = jsonPerson['fingerprint']
        email = jsonPerson['email']
        return cls(name, fingerprint, email)

    def jsonify(self):
        data = {'name' : self.name,
                'fingerprint' : self.fingerprint,
                'email' : self.email}
        return data
