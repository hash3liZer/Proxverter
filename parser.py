import os
import re
import sys
import yaml
from pull import PULL

pull = PULL()

class PARSER:

    DEF_PROTOTYPES = "/usr/share/proxverter/prototypes"
    REGEX_DOMAIN   = r"^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$"

    def __init__(self, prs):
        self.debug = prs.debug
        self.prototypes_path = prs.prototypes
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

    def validate_fields(self, _fields, _filename, *args):
        def _vald(_field):
            if _field not in _fields:
                pull.halt('Prototype: {} Reason: {} Err: "{}" field is not found'.format(
                    _filename, 'Invalid Syntax', _field
                ))

        for arg in args:
            _vald(arg)

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

        return _val

    def validate_field_proto(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "proto" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

        if _val != 'http' and _val != 'https':
            pull.halt('Prototype: {} Reason: {} Err: "proto" field allowed values [http, https]'.format(
                _filename, 'Value Error'
            ))

        return _val

    def validate_field_http_version(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "http_version" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

        if _val != '1.1' and _val != '2.0':
            pull.halt('Prototype: {} Reason: {} Err: "http_version" field allowed values [1.1, 2.0]'.format(
                _filename, 'Value Error'
            ))

        return _val

    def validate_field_landing(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "landing" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

    def validate_field_domains(self, _val, _filename):
        if not _val:
            pull.halt('Prototype: {} Reason: {} Err: "domains" field can\'t be left empty'.format(
                _filename, 'Value Error'
            ))

        for _domain in _val:
            if not re.match(self.REGEX_DOMAIN, _domain):
                pull.halt('Prototype: {} Reason: {} Err: "{}" is an invalid domain'.format(
                    _filename, 'Value Error', _domain
                ))

        return _val

    def validate(self):
        _checked = []                                   # Names of already checked Prototypes
        for prototype in self.prototypes:

            self.validate_fields(
                prototype.keys(),
                prototype.get('filename'),
                'creator',
                'name',
                'proto',
                'http_version',
                'landing',
                'domains',
                'substitutions',
                'cookies',
                'captures',
                'authentication'
            )

            for substitution in prototype.get('substitutions'):
                self.validate_fields(
                    substitution.keys(),
                    prototype.get('filename'),
                    'domain',
                    'search',
                    'replace',
                    'content_type'
                )

            for capture in prototype.get('captures'):
                self.validate_fields(
                    capture.keys(),
                    prototype.get('filename'),
                    'name',
                    'type'
                )

            if prototype.get('name') not in _checked:
                _checked.append(prototype.get('name'))

                self.prototypes[self.prototypes.index(prototype)]['creator'] = self.validate_field_creator(prototype.get('creator'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['name'] = self.validate_field_name(prototype.get('name'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['proto'] = self.validate_field_proto(prototype.get('proto'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['http_version'] = self.validate_field_http_version(prototype.get('http_version'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['landing'] = self.validate_field_landing(prototype.get('landing'), prototype.get('filename'))
                self.prototypes[self.prototypes.index(prototype)]['domains'] = self.validate_field_domains(prototype.get('domains'), prototype.get('filename'))
            else:
                pull.halt('Prototype: {} Reason: {} Err: Two prototypes with conflicting name "{}" detected'.format(
                    prototype.get('filename'), 'Conflicting Name', prototype.get('name')
                ))
