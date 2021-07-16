from OpenSSL import crypto, SSL

class Generator:

    def __init__(self, email=None, country=None, province=None, locality=None, organization=None, unit=None, commonname=None):
        self.email   = email or "admin@shellvoide.com"
        self.country = country or "PK"
        self.province = province or "Punjab"
        self.locality = locality or "en"
        self.organization = organization or "Proxverter"
        self.unit     = unit or "Proxy"
        self.commonname = commonname or "hash3liZer"
        self.serial_number = 0
        self.valid_start = 0
        self.valid_end   = 10*365*24*60*60

    def generate(self):
        self.cert = crypto.X509()
        self.key = crypto.PKey()
        self.key.generate_key(crypto.TYPE_RSA, 4096)
        self.cert.get_subject().C = self.country
        self.cert.get_subject().ST = self.province
        self.cert.get_subject().L = self.locality
        self.cert.get_subject().O = self.organization
        self.cert.get_subject().OU = self.unit
        self.cert.get_subject().CN = self.commonname
        self.cert.get_subject().emailAddress = self.email
        self.cert.set_serial_number(self.serial_number)
        self.cert.gmtime_adj_notBefore(self.valid_start)
        self.cert.gmtime_adj_notAfter(self.valid_end)
        self.cert.set_issuer(self.cert.get_subject())
        self.cert.set_pubkey(self.key)
        self.cert.sign(self.key, 'sha512')

    def gen_key(self, key_file):
        key_file = open(key_file, 'wt')
        try:
            key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key).decode("utf-8"))
        except TypeError:
            key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key))
        key_file.close()

    def gen_cert(self, cert_file):
        cert_file = open(cert_file, 'wt')
        try:
            cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert).decode("utf-8"))
        except TypeError:
            cert_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key))
        cert_file.close()
