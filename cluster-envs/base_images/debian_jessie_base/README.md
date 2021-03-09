# CVE 2015-3306 Base Image

Base docker image with the CVE 2015-3306 vulnerability.

## Description
The mod_copy module in ProFTPD 1.3.5 allows remote attackers to read and write to arbitrary files via the site cpfr and site cpto commands.    

## Useful commands

```bash
make all # Deletes the current image and re-builds it
make build # Builds the image
make rm-image # Deletes the image   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar