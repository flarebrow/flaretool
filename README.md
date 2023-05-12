# flaretool

**flaretool** is flarebrow Library.  

![](https://img.shields.io/badge/python-%3E%3D3.9-blue)

[API Doc](https://flarebrow.github.io/flaretool/)

**Attention**  
This library is under development and may exhibit unexpected behavior. New features will be released soon. Please stay tuned.


## install
```bash
pip install flaretool
```

## install (dev)
```bash
pip install -i https://test.pypi.org/simple/ flaretool
```

## usage

[NetTool Doc](https://flarebrow.github.io/flaretool/flaretool.nettool.html)

### NetTool sample
```python
from flaretool import nettool

network_info = nettool.get_global_ipaddr_info()
print("=== Your IP Infomation ===")
print("ip:", network_info.ipaddr)
print("hostname:", network_info.hostname)
print("country:", network_info.country)
```

### NetTool Command sample

```bash
flaretool nettool get_global_ipaddr_info
```

All methods within Netttol can be executed as commands.

