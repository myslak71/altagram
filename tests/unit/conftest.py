"""Starship crawler response fixtures."""
import pytest


@pytest.fixture
def databank_page() -> str:
    """Return HTML code for databank page."""
    return """<html>
<head>
    <title>Index empty link</title>
</head>
<body>
<a href="/wiki/Starship" title="Starship">Starship</a>
<ul>
    <li><a href="/wiki/Starship1" title="Starship1">Starship1</a>
        <ul>
            <li><a href="/wiki/Starship2" title="Starship2">Starship2</a></li>
        </ul>
    </li>
</ul>
</body>
</html>"""


@pytest.fixture
def starship1_page() -> str:
    """Return HTML code for first starship page."""
    return """<html>
<head>
    <title>Index empty link</title>
</head>
<body>
<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="hyperdrive">
    <ul>
        <li>Class 1.5</li>
        <li>Class 10 <a href="#cite_note-Collapse-1">&#91;1&#93;</a></li>
    </ul>
</div>
</body>
</html>"""


@pytest.fixture
def starship2_page() -> str:
    """Return HTML code for second starship page."""
    return """<html>
<head>
    <title>Index empty link</title>
</head>
<body>
<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="hyperdrive">
    <ul>
        <li>Class 5 (fresh)</li>
    </ul>
</div>
</body>
</html>"""
