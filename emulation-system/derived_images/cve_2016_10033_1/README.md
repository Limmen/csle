# CVE 2016-10033 Image

Docker image with the CVE 2010-10033 vulnerability.

## Description

PHPMailer before its version 5.2.18 suffer from a vulnerability that could lead to remote code execution (RCE).

## Useful commands

```bash
make all # Deletes the current image and re-builds it
make build # Builds the image
make rm-image # Deletes the image   
```

## Services

- SSH
- Apache2
- SMTPD

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar