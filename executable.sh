#!/bin/bash

find ./ -type f -regex '.*\.\(py\|sh\|bash\)$' -exec chmod +x {} +
