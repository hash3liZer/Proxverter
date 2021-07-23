![banner](https://user-images.githubusercontent.com/29171692/126787146-54fd3b6c-883b-4990-8cef-ba8816584bc4.png)

<h1 align="center">Proxverter</h1>
Cross platform system wide reverse proxy & TLS Interception library for Python. Basically a wrapper around proxy.py and PyOpenSSL allowing easy integration and certificate generation on command. 

## Features
<ul>
  <li><b>Cross Platform</b>: The library is cross platform and can be used on windows, linux and macos</li>
  <li><b>TLS Interception</b>: It's a wrapper against lightweight <code>proxy.py</code> by <a href="https://github.com/abhinavsingh/">@abhinavsingh</a> which provides many features and TLS-interception being one of them</li>
  <li><b>Custom Plugins</b>: Through the API you can provide custom plugins to intercept and modify data as per your needs. Document is given below</li>
  <li><b>System wide proxy</b>: The tool provides system wide proxy. You just have to call the API and the library will do the rest</li>
  <li><b>Certificate Generation</b>: You can generate self-signed certificate which is basically a wrapper around <code>pyopenssl</code></li>
</ul>
