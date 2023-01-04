---
title: Log files and Debugging
permalink: /docs/debugging/
---

## Log files and Debugging

Log files of physical servers in the management system are 
located at `/tmp/csle` and PID files are 
located at `/var/log/csle`. 
Log files of emulated devices are located at `/`.

To debug management services, check the log files and locate the error. 
Then try to fix the error and restart the services using the CLI. 
To debug emulated components, use SSH or `docker exec` 
to open a terminal inside the component and check the log files.

If you cannot resolve the issue, we recommend restarting all services 
and see if you can reproduce the issue. If you can reproduce the issue 
and you believe it is a bug, please file a bug report following 
the instructions listed <a href="../development-conventions">here</a>.
