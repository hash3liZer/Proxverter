import os
import sys
import yaml
from pull import PULL

pull = PULL()

class PARSER:

    DEF_PROTOTYPES = "/usr/share/proxverter/prototypes"

    def __init__(self, prs):
        self.prototypes = self.prototypes(prs.prototypes)

    def prototypes(self, _val):
        rtval = []
        dirnamer = ""

        if _val:
            if os.path.isdir(_val):
                dirnamer = os.path.join(os.path.dirname(__file__), _val)
            else:
                pull.halt("The provided prototypes directory doesn't exist!")
        else:
            if not os.path.isdir(self.DEF_PROTOTYPES):
                pull.halt("Unable to Locate Prototypes Directory")

            dirnamer = self.DEF_PROTOTYPES

        files = os.listdir(dirnamer)
        for file in files:
            file = os.path.join(dirnamer, file)
            if file.endswith(".yaml"):
                sfile = open(file)
                yfile = yaml.load(sfile, Loader=yaml.FullLoader)
                yfile['filename'] = file.split('/')[-1]
                rtval.append(yfile)
                sfile.close()

        return rtval

    def validate_fields(self, _fields, _filename):
        if 'creator' not in _fields:
            pull.halt('Prototype: {} Reason: {} Err: "creator" field is not found'.format(
                _filename, 'Invalid Syntax'
            ))

        if 'name' not in _fields:
            pull.halt('Prototype: {} Reason: {} Err: "name" field is not found'.format(
                _filename, 'Invalid Syntax'
            ))

        if 'proto' not in _fields:
            pull.halt('Prototype: {} Reason: {} Err: "proto" field is not found'.format(
                _filename, 'Invalid Syntax'
            ))

    def validate_field_creator(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "creator" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

        if not _val.startswith('@'):
            _val = '@' + _val

        _val = _val[:13] + '...' if len(_val) > 12 else _val
        return _val

    def validate_field_name(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "name" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

        if not _val.startswith('#'):
            _val = '#' + _val

        return _val

    def validate_field_proto(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "proto" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

        if _val != 'http':
            pull.halt('Prototype: {} Reason: {} Err: "proto" field allowed values [http,]'.format(
                _filename, 'Value Error'
            ))

        return _val

    def validate(self):
        _checked = []                                   # Names of already checked Prototypes
        for prototype in self.prototypes:
            keys = prototype.keys()
            self.validate_fields(keys, prototype.get('filename'))
            if prototype.get('name') not in _checked:
                _checked.append(prototype.get('name'))

                self.prototypes[self.prototypes.index(prototype)]['creator'] = self.validate_field_creator(prototype.get('creator'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['name'] = self.validate_field_name(prototype.get('name'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['proto'] = self.validate_field_proto(prototype.get('proto'), prototype.get('filename'))
            else:
                pull.halt('Prototype: {} Reason: {} Err: Two prototypes with conflicting name "{}" detected'.format(
                    prototype.get('filename'), 'Conflicting Name', prototype.get('name')
                ))
