# ETD-Bire
This program is used for evil twin attackes detection.
<p align="left">
<img src="https://img.shields.io/badge/Python-3-blue.svg"></a> <img src="https://img.shields.io/badge/license-GPLv3-red.svg">
</p>

## Requirements

Following are the requirements for getting the most out of ETD-Bire:

- A working Linux system. Kali Linux is the officially supported distribution, thus all features are primarily tested on this platform.
- One wireless network adapter that supports AP & Monitor mode and is capable of injection.(such as TL-WN722N)
- Software required:
	* Python 3.5+
	* wpa_supplicant (sudo apt-get install wpa_supplicant)
- Python-Libary required:
	* pyqt5 (pip install pyqt5)
	* scapy (pip intall scapy)
	* pywifi (pip install pywifi)
	
## Installation&Usage

After installing the prerequisites listed above for your platform, you can
run the following commands:

```bash
git clone https://github.com/oycillessen/ETD-Bire.git
cd ETD-Bire
sudo python3 main.py
```

## License

(C) oycillessen 2019, [GPL-3.0 License].

[GPL-3.0 License]: https://opensource.org/licenses/GPL-3.0

## Contact

You can send message to oycillessen@foxmail.com .
