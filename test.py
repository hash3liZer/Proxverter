import sys
import proxverter

p = proxverter.Proxverter(
    "127.0.0.1",
    8081,
    is_https=True
)

p.gen_key(open("priv.key", "wt"))
p.gen_cert(open("cert.crt", "wt"))
p.join()
