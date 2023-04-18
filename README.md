SubGPT looks at subdomains you have already discovered for a domain and uses BingGPT to predict and find more. Best part? It's free!

The following subdomains were found by this tool with [these](https://gist.githubusercontent.com/s0md3v/237f246ddbc17756a77837daaa1cc674/raw/5863caaa1c991aaf50c45acb25c226c7d8d776c0/input.txt) 30 subdomains as input.
```
call-prompts-staging.example.com
dclb02-dca1.prod.example.com
activedirectory-sjc1.example.com
iadm-staging.example.com
elevatenetwork-c.example.com
```

If you like my work, you can support me with as little as $1, [here](https://github.com/sponsors/s0md3v) :\)

### Install & Configuration
#### Installation
- with pip (recommended): `pip install subgpt`
- from github: `git clone https://github.com/s0md3v/SubGPT && cd SubGPT && python setup.py install`

#### Getting Bing Cookie
1. Install the cookie editor extension ([Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm), [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/))
2. Visit [bing.com](https://www.bing.com/), make sure you are logged in.
3. Open the extension and copy your cookie using the "export" button
4. Paste it in a file e.g. `cookies.json`
5. All set!

> Note: Any issues regarding BingGPT itself should be reported [EdgeGPT](https://github.com/acheong08/EdgeGPT), not here.

### Using SubGPT
The standard way to use SubGPT is as follows:
```
subgpt -i input.txt -o output.txt -c /path/to/cookies.json
```
If you don't specify an output file, the output will be shown in your terminal (`stdout`) instead.

To generate subdomains and not resolve them, use the `--dont-resolve` option. It's a great way to investigate SubGPT's capabilities.

### Important

1. Make sure your subdomains list only has subdomains from one domain. Each line in your file should contain one subdomain and nothing else.
2. Sometimes your cookie will expire if you visit bing.com often. In that case, just export and save it again.
3. SubGPT looks at A/CNAME records to determine whether a subdomain exists. It can also detect wildcard on first-level subdomains and handle it automatically. You can go through the code to see how its implemented if it concerns you.
4. It can't replace traditional sub-generators like [gotator](https://github.com/Josue87/gotator), [alterx](https://github.com/projectdiscovery/alterx), [dnsgen](https://github.com/ProjectAnte/dnsgen) etc. However, being powered by AI helps it to generate subdomains that these traditional tools can't.
