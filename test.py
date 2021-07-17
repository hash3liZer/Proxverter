import sys
import os
import tempfile
import proxverter
import logging
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()

    p = proxverter.Proxverter(
        "127.0.0.1",
        8081,
        is_https=True,
        verbose=True
    )

    fl1 = os.path.join(tempfile.gettempdir(), 'priv.key')
    fl2 = os.path.join(tempfile.gettempdir(), 'cert.crt')

    if not os.path.isfile(fl1) or not os.path.isfile(fl2):
        sys.exit("Error")

    p.gen_key(fl1)
    p.gen_cert(fl2)

    p.join(fl1, fl2)
