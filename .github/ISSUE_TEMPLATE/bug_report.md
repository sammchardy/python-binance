---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Code snippet to reproduce the behavior:

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**
 - Python version: [e.g. 3.5]
 - Virtual Env: [e.g. virtualenv, conda]
 - OS: [e.g. Mac, Ubuntu]
 - python-binance version

**Logs**
Please set logging to debug and paste any logs here, or upload `debug.log` file to the issue.
```python
import logging
# This will log to both console and file
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
handlers=[
logging.FileHandler('debug.log'),
logging.StreamHandler()
]
)
```

**Additional context**
Add any other context about the problem here.
