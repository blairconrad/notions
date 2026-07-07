# Notions
Oddments. Sundries.

Personal stuff that I didn't want to put anywhere else.

## Installing the Tools

Use [uv](https://docs.astral.sh/uv/) to install tools so they're available on your PATH.

### All tools

Installs `md2html` and all DICOM tools:

```sh
uv tool install path/to/notions
```

### DICOM tools only

```sh
uv tool install path/to/notions/Dicom
```

### Editable install (for development)

Changes to the Python source are picked up immediately without reinstalling:

```sh
uv tool install -e path/to/notions
```

### Updating after source changes

```sh
uv tool install --force path/to/notions
```
