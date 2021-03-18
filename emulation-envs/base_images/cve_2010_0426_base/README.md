# CVE 2010-0426 Base Image

Base docker image with the CVE 2010-0426 vulnerability.

## Description
The bug was found in sudoedit, which does not handle the 'sudoedit' command correctly, this allows a malicious user to replace the real sudoedit command with an arbitrary command.

Local attackers could exploit this issue to run arbitrary commands as the 'root' user. Successful exploits can completely compromise an affected computer.    

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