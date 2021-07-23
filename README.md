![banner](https://user-images.githubusercontent.com/29171692/126787146-54fd3b6c-883b-4990-8cef-ba8816584bc4.png)

<h1 align="center">Proxverter</h1>
Cross platform system wide proxy server & TLS Interception library for Python. Basically a wrapper around proxy.py and PyOpenSSL allowing easy integration and certificate generation on command. 

## Features
<ul>
  <li><b>Cross Platform</b>: The library is cross platform and can be used on windows, linux and macos</li>
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

### TLS Interception in non-SSL Mode
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

### TLS Interception in SSL Mode
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
