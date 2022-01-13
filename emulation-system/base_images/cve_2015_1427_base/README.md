# CVE-2015-1427 Base Image

Base docker image with the CVE 2015-1427 vulnerability.

## Description

The bug is found in the REST API, which does not require authentication, where the search function allows groovy code execution and its sandbox can be bypassed using `java.lang.Math.class.forName` to reference arbitrary classes. It can be used to execute arbitrary Java code. The bug is found in the REST API, which does not require authentication, where the search function allows groovy code execution and its sandbox can be bypassed using java.lang.Math.class.forName to reference arbitrary classes. It can be used to execute arbitrary Java code.    

## Useful commands

```bash
make all # Deletes the current image and re-builds it
make build # Builds the image
make rm-image # Deletes the image   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar