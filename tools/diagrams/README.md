# Build the illustrated technical flows

Readers need only Markdown and local PNGs. Each image is generated from the **same Mermaid sequence** kept under “Text and editable Mermaid sequence” in its pattern. Branches, numbering and return arrows are rendered by Mermaid, not drawn a second time. Official artwork is positioned over the actual participant ID; a [reviewed lifeline map](platforms.txt) identifies products, covered by the [icon terms](../../assets/platforms/README.md).

For authors: use Node.js 22+ and a local Google Chrome installation. From the repository root:

```sh
npm ci --prefix tools/diagrams --ignore-scripts
npm --prefix tools/diagrams run render
npm --prefix tools/diagrams test
python3 -m unittest discover -s tests -v
```

Set `CHROME_PATH` if the Chrome executable isn't in its standard location. Dependency installation needs internet access; rendering then runs with networking disabled. `test` renders all entry and shared-guide Mermaid sources in Chrome, checks participant IDs, icon integrity, and the input and PNG fingerprints without rewriting output. Fonts and Chrome versions can change antialiasing between machines; review PNG changes before committing. For a new entry, add its flow-image Markdown link and a `platforms.txt` row explicitly mapping **every** participant ID (`-` means no platform), then regenerate. Never put access keys, environment IDs or tenant data in an example.

The repository's [Git attributes](../../.gitattributes) keep diagram text and fingerprint inputs at LF even in Windows checkouts with `core.autocrlf=true`. Keep your editor on LF for those files. Official SVGs and published PNGs retain their original bytes; do not normalize or re-export them to fix a fingerprint failure.
