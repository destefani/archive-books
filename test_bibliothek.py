import os
from pathlib import Path
import tempfile

import bibliothek


def test_convert_jp2_to_png():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        test_image = Path("tests/ljs389_0000.png")
        bibliothek.convert_jp2_to_png(test_image, temp_dir / "test.png")
        assert os.path.exists(temp_dir / "test.png")
