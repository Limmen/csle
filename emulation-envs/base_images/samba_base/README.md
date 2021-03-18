# SambaCry Base Image

Samba base docker image, used for implementing sambacry cve-2017-7494 vulnerabilities  

## Description

Samba in 4.5.9 version and before that is vulnerable to a remote code execution vulnerability named SambaCry. CVE-2017-7494 allows remote authenticated users to upload a shared library to a writable shared folder, and perform code execution attacks to take control of servers that host vulnerable Samba services.

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

(C) 2020, Kim Hammar