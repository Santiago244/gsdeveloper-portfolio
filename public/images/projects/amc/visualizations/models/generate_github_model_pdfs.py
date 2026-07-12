"""Generate PlotNeuralNet diagrams for the models in ``github-models``.

The script writes one TeX file per architecture and compiles it to PDF when
``pdflatex`` is available on PATH. It intentionally does not import the model
classes, so the visualization stays independent from training dependencies.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import shutil
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PLOTNEURALNET = HERE / "PlotNeuralNet"
sys.path.insert(0, str(PLOTNEURALNET))

from pycore.tikzeng import (  # noqa: E402
    to_Conv,
    to_ConvConvRelu,
    to_Pool,
    to_SoftMax,
    to_Sum,
    to_begin,
    to_connection,
    to_cor,
    to_end,
    to_generate,
    to_head,
    to_skip,
)


NUM_CLASSES = 24
INPUT_LEN = 1024


def _header() -> list[str]:
    return [
        to_head("PlotNeuralNet"),
        to_cor(),
        r"""
\def\LstmColor{rgb:green,5;blue,2;white,6}
\def\DenseColor{rgb:blue,5;red,2.5;white,5}
\def\CatColor{rgb:blue,3;green,12;white,5}
""",
        to_begin(),
    ]


def _box(
    name: str,
    caption: str,
    *,
    s_filer: str = " ",
    n_filer: str = " ",
    offset: str = "(0,0,0)",
    to: str = "(0,0,0)",
    width: float = 1.0,
    height: float = 20.0,
    depth: float = 20.0,
    fill: str = r"\DenseColor",
    opacity: float = 0.9,
) -> str:
    return rf"""
\pic[shift={{{offset}}}] at {to}
    {{Box={{
        name={name},
        caption={{{caption}}},
        xlabel={{{{{n_filer}, }}}},
        zlabel={{{s_filer}}},
        fill={fill},
        opacity={opacity},
        height={height},
        width={width},
        depth={depth}
        }}
    }};
"""


def _concat(name: str, *, offset: str, to: str) -> str:
    return rf"""
\pic[shift={{{offset}}}] at {to}
    {{Ball={{
        name={name},
        fill=\CatColor,
        opacity=0.75,
        radius=2.0,
        logo=$\oplus$
        }}
    }};
"""


def _write_arch(name: str, arch: list[str]) -> Path:
    tex_path = HERE / f"{name}.tex"
    with contextlib.redirect_stdout(io.StringIO()):
        to_generate(arch + [to_end()], str(tex_path))
    return tex_path


def _compile_pdf(tex_path: Path, *, runs: int = 1) -> bool:
    if shutil.which("pdflatex") is None:
        print(f"pdflatex not found; wrote {tex_path.name} only.")
        return False

    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        tex_path.name,
    ]
    for _ in range(runs):
        subprocess.run(command, cwd=HERE, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return True


def cldnn_like_arch() -> list[str]:
    arch = _header()
    arch.extend(
        [
            _box(
                "input",
                r"\scriptsize I/Q input",
                s_filer=str(INPUT_LEN),
                n_filer="2",
                width=1.0,
                height=16,
                depth=48,
                fill=r"\ConvColor",
            ),
            to_ConvConvRelu(
                "conv1",
                s_filer=INPUT_LEN,
                n_filer=(64, 64),
                offset="(1.4,0,0)",
                to="(input-east)",
                width=(2, 2),
                height=24,
                depth=48,
                caption=r"\scriptsize Conv1D k8",
            ),
            to_connection("input", "conv1"),
            to_Pool(
                "pool1",
                offset="(0.2,0,0)",
                to="(conv1-east)",
                width=1,
                height=22,
                depth=38,
                caption=r"\scriptsize MaxPool",
            ),
            to_ConvConvRelu(
                "conv2",
                s_filer=512,
                n_filer=(64, 64),
                offset="(1.2,0,0)",
                to="(pool1-east)",
                width=(2, 2),
                height=24,
                depth=38,
                caption=r"\scriptsize Conv1D k8",
            ),
            to_connection("pool1", "conv2"),
            to_Pool("pool2", offset="(0.2,0,0)", to="(conv2-east)", height=21, depth=30, caption=r"\scriptsize MaxPool"),
            to_ConvConvRelu(
                "conv3",
                s_filer=256,
                n_filer=(64, 64),
                offset="(1.2,0,0)",
                to="(pool2-east)",
                width=(2, 2),
                height=24,
                depth=30,
                caption=r"\scriptsize Conv1D k8",
            ),
            to_connection("pool2", "conv3"),
            to_Pool("pool3", offset="(0.2,0,0)", to="(conv3-east)", height=20, depth=24, caption=r"\scriptsize MaxPool"),
            to_ConvConvRelu(
                "conv4",
                s_filer=128,
                n_filer=(64, 64),
                offset="(1.2,0,0)",
                to="(pool3-east)",
                width=(2, 2),
                height=24,
                depth=24,
                caption=r"\scriptsize Conv1D k8",
            ),
            to_connection("pool3", "conv4"),
            to_Pool("pool4", offset="(0.2,0,0)", to="(conv4-east)", height=19, depth=18, caption=r"\scriptsize MaxPool"),
            _box(
                "lstm1",
                r"\scriptsize LSTM",
                s_filer=64,
                n_filer="50",
                offset="(1.3,0,0)",
                to="(pool4-east)",
                width=2.2,
                height=18,
                depth=18,
                fill=r"\LstmColor",
            ),
            to_connection("pool4", "lstm1"),
            _box(
                "lstm2",
                r"\scriptsize LSTM",
                s_filer=64,
                n_filer="50",
                offset="(1.1,0,0)",
                to="(lstm1-east)",
                width=2.2,
                height=18,
                depth=18,
                fill=r"\LstmColor",
            ),
            to_connection("lstm1", "lstm2"),
            _box("dense", r"\scriptsize Dense SELU Dropout", s_filer=" ", n_filer="128, 128", offset="(1.2,0,0)", to="(lstm2-east)", width=2.2, height=16, depth=16),
            to_connection("lstm2", "dense"),
            to_SoftMax("softmax", NUM_CLASSES, offset="(1.1,0,0)", to="(dense-east)", height=14, depth=14, caption=r"\scriptsize Softmax"),
            to_connection("dense", "softmax"),
        ]
    )
    return arch


def mcldnn_arch() -> list[str]:
    arch = _header()
    arch.extend(
        [
            _box(
                "input",
                r"\scriptsize I/Q input",
                s_filer=str(INPUT_LEN),
                n_filer="2",
                width=1.0,
                height=16,
                depth=46,
                fill=r"\ConvColor",
            ),
            to_Conv(
                "conv_iq",
                s_filer=INPUT_LEN,
                n_filer=50,
                offset="(1.4,2.1,0)",
                to="(input-east)",
                width=2,
                height=22,
                depth=42,
                caption=r"\scriptsize Conv2D 2x8",
            ),
            to_Conv(
                "conv_i",
                s_filer=INPUT_LEN,
                n_filer=50,
                offset="(1.4,0,0)",
                to="(input-east)",
                width=2,
                height=18,
                depth=42,
                caption=r"\scriptsize I causal Conv1D",
            ),
            to_Conv(
                "conv_q",
                s_filer=INPUT_LEN,
                n_filer=50,
                offset="(1.4,-2.1,0)",
                to="(input-east)",
                width=2,
                height=18,
                depth=42,
                caption=r"\scriptsize Q causal Conv1D",
            ),
            to_connection("input", "conv_iq"),
            to_connection("input", "conv_i"),
            to_connection("input", "conv_q"),
            _concat("cat_iq", offset="(1.4,-1.0,0)", to="(conv_i-east)"),
            to_connection("conv_i", "cat_iq"),
            to_connection("conv_q", "cat_iq"),
            to_Conv(
                "conv_pair",
                s_filer=INPUT_LEN,
                n_filer=50,
                offset="(1.1,0,0)",
                to="(cat_iq-east)",
                width=2,
                height=22,
                depth=42,
                caption=r"\scriptsize Conv2D 1x8",
            ),
            to_connection("cat_iq", "conv_pair"),
            _concat("cat_all", offset="(1.4,1.0,0)", to="(conv_pair-east)"),
            to_connection("conv_iq", "cat_all"),
            to_connection("conv_pair", "cat_all"),
            to_Conv(
                "conv4",
                s_filer=1020,
                n_filer=100,
                offset="(1.2,0,0)",
                to="(cat_all-east)",
                width=3,
                height=28,
                depth=34,
                caption=r"\scriptsize Conv2D 2x5",
            ),
            to_connection("cat_all", "conv4"),
            _box(
                "seq",
                r"\scriptsize squeeze transpose",
                s_filer=1020,
                n_filer="100",
                offset="(1.0,0,0)",
                to="(conv4-east)",
                width=1.2,
                height=22,
                depth=24,
                fill=r"\DenseColor",
            ),
            to_connection("conv4", "seq"),
            _box(
                "lstm1",
                r"\scriptsize LSTM",
                s_filer=1020,
                n_filer="128",
                offset="(1.1,0,0)",
                to="(seq-east)",
                width=2.3,
                height=22,
                depth=24,
                fill=r"\LstmColor",
            ),
            to_connection("seq", "lstm1"),
            _box(
                "lstm2",
                r"\scriptsize LSTM",
                s_filer=1020,
                n_filer="128",
                offset="(1.0,0,0)",
                to="(lstm1-east)",
                width=2.3,
                height=22,
                depth=24,
                fill=r"\LstmColor",
            ),
            to_connection("lstm1", "lstm2"),
            _box("dense", r"\scriptsize Dense SELU Dropout", n_filer="128, 128", offset="(1.2,0,0)", to="(lstm2-east)", width=2.2, height=18, depth=18),
            to_connection("lstm2", "dense"),
            to_SoftMax("softmax", NUM_CLASSES, offset="(1.1,0,0)", to="(dense-east)", height=15, depth=15, caption=r"\scriptsize Softmax"),
            to_connection("dense", "softmax"),
        ]
    )
    return arch


def mcnet_arch() -> list[str]:
    arch = _header()
    arch.extend(
        [
            _box(
                "input",
                r"\scriptsize I/Q input",
                s_filer=str(INPUT_LEN),
                n_filer="2",
                width=1.0,
                height=16,
                depth=46,
                fill=r"\ConvColor",
            ),
            to_Conv(
                "stem",
                s_filer=512,
                n_filer=64,
                offset="(1.3,0,0)",
                to="(input-east)",
                width=2.2,
                height=24,
                depth=40,
                caption=r"\scriptsize Conv2D 3x7 s2",
            ),
            to_connection("input", "stem"),
            to_Pool("pool1", offset="(0.2,0,0)", to="(stem-east)", height=22, depth=32, caption=r"\scriptsize MaxPool"),
            _concat("precat", offset="(1.0,0,0)", to="(pool1-east)"),
            to_connection("pool1", "precat"),
            _box(
                "pre",
                r"\scriptsize pre branches 3x1 avg and 1x3",
                s_filer=128,
                n_filer="64",
                offset="(1.1,0,0)",
                to="(precat-east)",
                width=2.2,
                height=24,
                depth=28,
                fill=r"\ConvColor",
            ),
            to_connection("precat", "pre"),
            _box(
                "blocka",
                r"\scriptsize M block A downsample",
                s_filer=64,
                n_filer="128",
                offset="(1.2,0,0)",
                to="(pre-east)",
                width=2.8,
                height=26,
                depth=24,
                fill=r"\ConvColor",
            ),
            to_connection("pre", "blocka"),
            _box(
                "blockb",
                r"\scriptsize M block B residual",
                s_filer=64,
                n_filer="128",
                offset="(1.2,0,0)",
                to="(blocka-east)",
                width=2.8,
                height=26,
                depth=24,
                fill=r"\ConvColor",
            ),
            to_connection("blocka", "blockb"),
            to_skip("blocka", "blockb", pos=1.25),
            _box(
                "blockc",
                r"\scriptsize M block C downsample",
                s_filer=32,
                n_filer="128",
                offset="(1.2,0,0)",
                to="(blockb-east)",
                width=2.8,
                height=26,
                depth=20,
                fill=r"\ConvColor",
            ),
            to_connection("blockb", "blockc"),
            to_skip("blockb", "blockc", pos=1.25),
            _box(
                "blockd",
                r"\scriptsize M block D residual",
                s_filer=32,
                n_filer="128",
                offset="(1.2,0,0)",
                to="(blockc-east)",
                width=2.8,
                height=26,
                depth=20,
                fill=r"\ConvColor",
            ),
            to_connection("blockc", "blockd"),
            to_skip("blockc", "blockd", pos=1.25),
            _box(
                "blocke",
                r"\scriptsize M block E downsample",
                s_filer=16,
                n_filer="128",
                offset="(1.2,0,0)",
                to="(blockd-east)",
                width=2.8,
                height=26,
                depth=16,
                fill=r"\ConvColor",
            ),
            to_connection("blockd", "blocke"),
            to_skip("blockd", "blocke", pos=1.25),
            _box(
                "blockf",
                r"\scriptsize M block F 3 branch",
                s_filer=8,
                n_filer="256",
                offset="(1.2,0,0)",
                to="(blocke-east)",
                width=3.2,
                height=30,
                depth=14,
                fill=r"\ConvColor",
            ),
            to_connection("blocke", "blockf"),
            _concat("finalcat", offset="(1.0,0,0)", to="(blockf-east)"),
            to_connection("blockf", "finalcat"),
            to_skip("blocke", "finalcat", pos=1.35),
            _box(
                "gpool",
                r"\scriptsize global avg pool",
                s_filer=1,
                n_filer="384",
                offset="(1.0,0,0)",
                to="(finalcat-east)",
                width=1.4,
                height=18,
                depth=12,
                fill=r"\PoolColor",
            ),
            to_connection("finalcat", "gpool"),
            _box("fc", r"\scriptsize dropout dense", n_filer=str(NUM_CLASSES), offset="(1.1,0,0)", to="(gpool-east)", width=1.8, height=14, depth=14),
            to_connection("gpool", "fc"),
            to_SoftMax("softmax", NUM_CLASSES, offset="(1.0,0,0)", to="(fc-east)", height=13, depth=13, caption=r"\scriptsize logits"),
            to_connection("fc", "softmax"),
        ]
    )
    return arch


ARCHITECTURES = {
    "cldnn_like": cldnn_like_arch,
    "mcldnn": mcldnn_arch,
    "mcnet": mcnet_arch,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "models",
        nargs="*",
        choices=sorted(ARCHITECTURES),
        default=None,
        help="Specific diagrams to generate. Defaults to all github-models diagrams.",
    )
    parser.add_argument(
        "--tex-only",
        action="store_true",
        help="Only write TeX files; do not call pdflatex.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected_models = args.models or sorted(ARCHITECTURES)
    generated: list[Path] = []
    compiled: list[Path] = []

    for model_name in selected_models:
        tex_path = _write_arch(model_name, ARCHITECTURES[model_name]())
        generated.append(tex_path)
        if not args.tex_only and _compile_pdf(tex_path):
            compiled.append(tex_path.with_suffix(".pdf"))

    print("Generated TeX:")
    for path in generated:
        print(f"  {path.relative_to(HERE)}")

    if compiled:
        print("Compiled PDFs:")
        for path in compiled:
            print(f"  {path.relative_to(HERE)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
