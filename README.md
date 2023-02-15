# duplicated2link

A tiny python script to convert duplicated files to symbolic/hard links.

## Usage

```
python duplicated2link.py YOUR_DIR < -t soft(defailt)/hard > < --hash md5(default)/sha1/sha256/sha512 >
```

## Environment

Tested on Windows 10 with Python 3.9

## Existed Issues And TODOs

- [ ] Recognize existing symbolic links
- [ ] Recognize/Sort by file names and leave the better ones
- [ ] Support multi directories
- [ ] Multi-threading, etc.

## License
GNU General Public License