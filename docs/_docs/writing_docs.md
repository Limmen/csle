---
title: Writing Documentation
permalink: /docs/writing-docs/
---

## Writing Documentation

There are three kinds of documentation in CSLE:

- Release documentation (the document you are reading now). This document is generated for each major release only. It is a PDF generated through LaTeX.
- Live <a href="ttps://limmen.dev/csle/">web documentation</a>. This documentation is generated with Ruby. The source files are located at `csle/docs`. This documentation is updated automatically on every code commit to the project. To generate the web documentation manually, run the command:
   ```bash
   bundle exec Jekyll serve
   ```
  <p class="captionFig">
  Listing 133: Command to generate the web documentation at <a href="https://limmen.dev/csle/">https://limmen.dev/csle/</a>.
  </p>
- Python API documentation. This documentation is generated automatically from code comments using `sphinx`. To generate the API documentation, run the command:
   ```bash
   simulation-system/libs/generate_docs.sh
   ```
  <p class="captionFig">
   Listing 134: Command to generate the Python API documentation.
  </p>
