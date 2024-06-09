# SP-editor

Empowering Structural Engineers with Seamless Communication Between SpColumn and ETABS

## Installation

This isn't installed with PIP. Instead,
checkout the GitHub repository.

After checkout, use the ``pyproject.toml``
to install the needed development components.

```bash
python -m pip install -e .
```

Or to install via ``requirements-dev.txt``

```bash
python -m pip install -r requirements-dev.txt
```
Please add any installed packages to ``pyproject.toml``in **_dependencies[]_** section
then re-run .

```bash
 pip-compile --extra=dev --output-file=requirements-dev.txt
```

Please create your own branch and then merge change with ``main`` branch
## What is this Software about?

Sp-editor covers the following exciting features:

* Extract wall pier geometry defined in Etabs and transform to (X, Y) coordinates
* Extract pier design forces from Etabs and convert to SpColumn format
* Get user input of reinforcement pattern
* Run Batch processing and export demand capacity ratio results and PMM chart
* Provide complete SpColumn file for detailed design at later phases(ie., 100DD or CD).

## Demonstration

## Testing

## Documentation