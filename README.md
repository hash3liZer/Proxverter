![banner](https://user-images.githubusercontent.com/29171692/126787146-54fd3b6c-883b-4990-8cef-ba8816584bc4.png)

<h1 align="center">Proxverter</h1>
Cross platform system wide proxy server & TLS Interception library for Python. Basically a wrapper around proxy.py and PyOpenSSL allowing easy integration and certificate generation on command. 

## Features
<ul>
  <li><b>Cross Platform</b>: The library is cross platform and can be used on windows, linux and macos</li>
  <li><b>HTTP Interception</b>: You can intercept, capture and cache HTTP traffic through this. </li>
  <li><b>TLS Interception</b>: It's a wrapper against lightweight <code>proxy.py</code> by <a href="https://github.com/abhinavsingh/">@abhinavsingh</a> which provides many features and TLS-interception being one of them</li>
  <li><b>Custom Plugins</b>: Through the API you can provide custom plugins to intercept and modify data as per your needs. Documentation regarding plugin development is given below</li>
  <li><b>System wide proxy</b>: The tool provides system wide proxy. You just have to call the API and the library will do the rest</li>
  <li><b>Certificate Generation</b>: You can generate self-signed certificate which is basically a wrapper around <code>pyopenssl</code></li>
  <li><b>Flexible</b>: The underlying code of Proxverter is documented and quite easy to understand and edit. The code can further be developer and reused easily. </li>
  <li><b>Lightweight</b>: Thanks to `proxy.py`, unlike `mitmproxy` and other interception tools, proxverter is lightweight and doesn't really carry that much space around. </li>
  <li><b>Modifying data on the fly</b>: Since the library support TLS interception, the plugins can be used to modify data on the fly or reject any kind of request. </li>
</ul>

## Installation
### Latest version from GitHub

```bash
$ git clone https://github.com/hash3liZer/Proxverter.git
$ cd Proxverter/
$ python3 setup.py install
```

## Getting Started
After installation, you should be able to import `proxverter` on your python terminal. As of now, the library has 2 major sub modules which are: `certgen` and `sysprox`. The use of both of them is disucussed in the later sections. 

### HTTP Interception
```python
import proxverter
prox = proxverter.Proxverter(ip="127.0.0.1", port=8081, verbose=True)    ## Verbose mode will also show logs
prox.set_sysprox()                                                         ## Set system wide proxy
prox.engage()                                                              ## Press CTRL+C to move further
prox.del_sysprox()                                                         ## Remove system wide proxy
```

This will start proxy server in the background. Now, you can verify the working of proxy using `curl`:
```bash
$ curl -L -x 127.0.0.1:8081 http://www.google.com
```

### TLS Interception (HTTPS)
```python
import proxverter
prox = proxverter.Proxverter(ip="127.0.0.1", port=8081, is_https=True, verbose=True)    ## Verbose mode will also show logs

## Get certificate
prox.fetch_cert("/tmp/certificate.pem")                      

prox.set_sysprox()                                                         ## Set system wide proxy
prox.engage()                                                              ## Press CTRL+C to move further
prox.del_sysprox()                                                         ## Remove system wide proxy
```

The line `prox.fetch_cert` will generate a certificate at `/tmp/certificate.pem`. You need to import this certifcate in system root keychain or browser ceritifcates in order to capture TLS traffic. 

Sometimes, you might want to get the `pfx` version of the certifcate to be imported in windows root keychain. You can get the `pfx` using following method: 
```python
prox.fetch_pfx("/tmp/certificate.pfx")
```

Altough, there would be no need of private key for this to capture the traffic. However, if for some reason, you need private key as well. You can call the following method: 
```python
prox.fetch_pkey("/tmp/key.pem")
```

The certificates and key are only generated for the first time the library is called. After that when you call the `engage` method, the previous certificates will be used. However, if you want to refresh certifcates and have newly generated certs, you have to pass the option `new_certs=True` to `Proxverter` instance: 

```python
prox = proxverter.Proxverter(ip="127.0.0.1", port=8081, new_certs=True)
```

The TLS interception for SSL mode can be tested using this command:
```bash
$ curl -L -x 127.0.0.1:8081 https://www.google.com
```

### Interception with automatic system wide proxy
By default, when you call the `engage` method, proxvetrer will not automatically create a system wide proxy cache or in other words, you will have to setup the proxy yourself for the software you are targeting.

However, if you do want the proxverter to handle this case for you and create a system wide proxy cache i.e. traffic from the host will pass through our proxverter instance, you will have to pass the argument `sysprox=True` to `Proxverter` instance: 

```python
import proxverter
prox = proxverter.Proxverter(ip="127.0.0.1", port=8081, sysprox=True)

prox.engage()
...
```

### Verbose mode
Let's talk about logs from `proxy.py` tool. By default when the proxverter instance is created, all the logs are suppressed. However, you will be able to see the errors if occured any from `proxy.py`. For this we have argument: `verbose`. If you want to see the all the logs especially from `proxy.py`, you can set `verbose=True` in proxverter instance: 

```python
import proxverter
prox = proxverter.Proxverter(ip="127.0.0.1", port=8081, verbose=True)
prox.engage()
```

## Generating Self Signed Certificates
Besides from TLS Interception, another purpose of `proxverter` is to generate certificates on command. This is different from the certificates and keys generated by `Proxverter` instance. 

```python
from proxverter.certgen import Generator

gen = Generator()
gen.generate()         ## Generate certificate and stores in memory

gen.gen_key("/tmp/key.pem")     ## Public Certificate
gen.gen_cert("/tmp/cert.pem")   ## Private Key
gen.gen_pfx("/tmp/cert.pfx")    ## Certificate in PFX format to be be imported in windows keychain
```

This would generate credentials for a single certificate. If you need another certificate, you will need to create a separate instance. For example, if you want to generate 2 certificates, then: 

```python
from proxverter.certgen import Generator

gen1 = Generator()
gen2 = Generator()

...
```

### Self Signed certificate with custom fields
A certificate accepts a number of fields like email, country, unit name etc. By default all these fields are left empty. However, you can specify these fields in `Generator` instance. 

```python
from proxverter.certgen import Generator

gen = Generator(
  email="admin@shellvoide.com",
  country="PK",                      ## Country code here
  province="Islamabad Capital Territory",
  locality="Islamabad",
  organization="localhost",
  unit="localhost",
  commonname="example.com"
)
gen.generate()

...
```

## System wide proxy
Like other usages, `proxverter` can also be used to create a system wide proxy. This allows the host to forward all the traffic of the host to the proxy that was mentioned in system wide proxy instance. 

```python
from proxverter.sysprox import Proxy

## Setting system wide proxy
sprox = Proxy(ip_address="127.0.0.1", port=8081)
sprox.engage()

...
## Do the stuff here while system wide proxy is on
...

## Removing system wide proxy
sprox.cleanup()
```

## Custom Plugins
Plugins are the building block of proxverter or in other words the library named: `proxy.py`. These plugins can be used side by side with the main proxy to provide extra functionality to the current working proxy instance. 

