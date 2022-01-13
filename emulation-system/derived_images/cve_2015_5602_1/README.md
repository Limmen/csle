# CVE 2015-5602 Image

Docker image with the CVE 2015-5602 vulnerability.

## Description
The bug was found in sudoedit, which does not check the full path if a wildcard is used twice 
(e.g. `/home/*/*/esc.txt`), this allows a malicious user to replace the esc.txt real file with a symbolic link to a different location 
(e.g. `/etc/shadow`).

Successfully exploiting this issue may allow an attacker to mpvsulate files and to gain root privileges 
on host system through symlink attacks.        

## Useful commands

```bash
make all # Deletes the current image and re-builds it
make build # Builds the image
make rm-image # Deletes the image   
```

## Services

- SSH

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar