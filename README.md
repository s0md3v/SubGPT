SubGPT takes subdomains you have already discovered for a target and uses BingGPT to predict what other subdomains are likely to exists. It's free as it uses Microsoft Bing.

Like the tool? Support my work for as little as $1, [here](https://github.com/sponsors/s0md3v) :\)

### Install & Configuration
#### Installation
- with pip (recommended): `pip install subgpt`
- from github: `git clone https://github.com/s0md3v/SubGPT && cd SubGPT && python setup.py install`

#### Getting Bing Cookie
1. Install 
2. Visit bing.com
3. Open the extension and copy your cookies using the "export" button
4. Paste it in a file e.g. `cookies.json`
5. Done. Now you can

> Note: Any issues regarding BingGPT itself should be reported [EdgeGPT](https://github.com/acheong08/EdgeGPT), not here.

### Using SubGPT

#### Find Subdomains
```
subgpt -i input.txt -o output.txt -c /path/to/cookies.json
```

#### Generate Subdomains
If you just want to generate subdomains and not resolve them, use this option:
```
subgpt -i input.txt -o output.txt -c /path/to/cookies.json --dont-resolve
```

#### Important

1. Sometimes your cookie will expire if you visit bing.com. In that case, just export it again.
2. Make sure your subdomains list only has subdomains from one domain.
3. SubGPT looks at A/CNAME records to determine whether a subdomain exists. It can also detect wildcard on first-level subdomains and handle it automatically. You can go through the code to see how its implemented if it concerns you.
4. It can't replace traditional sub-generators like [gotator](https://github.com/Josue87/gotator), [alterx](https://github.com/projectdiscovery/alterx), [dnsgen](https://github.com/ProjectAnte/dnsgen) etc. However, being powered by AI helps it generate subdomains that may not exist.
