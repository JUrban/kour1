#!/usr/bin/env python3
"""Package existing finite proofs and render the 19 representative derivations.

Run from a full research checkout. All copies are byte-identical; this script
does not mutate the historical research artifacts.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
ANC = PAPER / "ancillary"
sys.path.insert(0, str(ROOT / "scripts"))
from verify_19_62_monomial_certificates import verify_case
from render_19_62_rank_two import coordinate, SELECTED


def main():
    paths = [Path("scripts") / (name + ".py") for name in [
        "verify_19_62_monomial_certificates", "verify_19_62_rank_two",
        "verify_19_61_square_completion", "check_19_62_g2_integer_constants"]]
    for kind in SELECTED:
        paths.append(Path(f"results/19.62-{kind}-monomial-input.json"))
        for suffix in ["input.json", "certificate.jsonl", "short-certificate.jsonl"]:
            paths.append(Path(f"results/19.62-{kind}-rank-two-{suffix}"))
        for suffix in ["input.json", "certificate.jsonl"]:
            paths.append(Path(f"results/19.61-{kind}-square-completion-{suffix}"))
    paths.append(Path("results/19.61-g2-integral.grows"))
    paths.append(Path("results/19.62-g2-monomial-certificates.jsonl"))
    manifest = []
    for path in paths:
        destination = ANC / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, destination)
        raw = destination.read_bytes()
        manifest.append({"path": str(path), "bytes": len(raw),
                         "sha256": hashlib.sha256(raw).hexdigest()})
    (ANC / "manifest.json").write_text(json.dumps({
        "source_revision": "cff2c37b9bf6b737e8ad5f7ead12291a551b5201",
        "files": manifest}, indent=2) + "\n")
    out = [r"""\section{Nineteen representative carpet derivations}
\label{app:carpet-tables}
These tables complete the displayed finite proof of
\eqref{eq:derived-square}. A coordinate pair \((m,n)\) denotes
\(ma+nb\), for simple roots \(a,b\), with \(a\) short in \(B_2,G_2\).
Each initial variable lies in the specified entry of \(A\).
Every subsequent line lies in \(B\) at its root, hence also in \(A\).
An application column records a Chevalley rule on earlier lines.
Two applications on the same line have the stated coefficient gcd;
Bezout's identity gives the element in the second column.
The displayed final element has coefficient dividing the requested
coefficient. Tables use one destination root of each length.
Weyl transport, checked on all absolute rules, covers the other roots.
The ancillary files also check all 104 targets without this reduction.
"""]
    displayed = 0
    for kind in SELECTED:
        prefix = ROOT / f"results/19.62-{kind}-rank-two-"
        data = json.loads(Path(str(prefix) + "input.json").read_text())
        nr = len(data["roots"])
        for index, nodes in map(json.loads, Path(str(prefix) + "short-certificate.jsonl").read_text().splitlines()):
            verify_case(data, index, nodes)
            case = data["cases"][index - 1]
            if case["root"] not in SELECTED[kind]:
                continue
            displayed += 1
            names = {v[0]: i for i, v in enumerate(nodes, 1)}
            known = {v[0]: v for v in nodes}
            root = lambda r: "(" + ",".join(map(str, coordinate(kind, data["roots"][r]))) + ")"
            out.append(r"\par\medskip\noindent\begin{minipage}{\textwidth}" + "\n")
            out.append(r"\textbf{\(" + kind[0].upper() + "_" + kind[1] + r"\), request " + str(index) +
                       r": \(p=" + root(case["root"]) + r"\).} Requested coefficient " + str(case["coefficient"]) + ".\n")
            out.append(r"\(\ " + ",\\ ".join(f"X_{i}\\in A_{{{root(r)}}}" for i, (r, _) in enumerate(case["variables"], 1)) + r".\)\par" + "\n")
            out.append(r"\smallskip\centering\small\begin{tabular}{@{}llll@{}}\toprule" + "\n")
            out.append(r"Line & Element & Root & Applications\\\midrule" + "\n")
            for key, a, b, var, left, right in nodes:
                code, r = divmod(key, nr)
                parts = []
                for k, (_, bound) in enumerate(case["variables"], 1):
                    code, exponent = divmod(code, bound + 1)
                    if exponent:
                        parts.append(f"X_{k}" + (f"^{{{exponent}}}" if exponent > 1 else ""))
                coefficient = 2**a * 3**b
                element = (str(coefficient) if coefficient != 1 else "") + "".join(parts)
                applications = []
                coefficients = []
                if var >= 0:
                    reason = r"\text{initial}"
                else:
                    for edge in [left, right]:
                        rule, lk, rk = edge
                        _, _, _, i, j, c = data["rules"][rule]
                        expression = (str(c) if c != 1 else "") + f"z_{{{names[lk]}}}" + (f"^{{{i}}}" if i > 1 else "")
                        expression += f"z_{{{names[rk]}}}" + (f"^{{{j}}}" if j > 1 else "")
                        if expression not in applications:
                            applications.append(expression)
                        lc = 2**known[lk][1] * 3**known[lk][2]
                        rc = 2**known[rk][1] * 3**known[rk][2]
                        coefficients.append(c * lc**i * rc**j)
                    reason = r";\ ".join(applications)
                    if len(applications) > 1:
                        reason += r";\ \gcd(" + ",".join(map(str, coefficients)) + ")=" + str(coefficient)
                out.append(r"\(z_{" + str(names[key]) + r"}\) & \(" + element + r"\) & \(" +
                           root(r) + r"\) & \(" + reason + r"\) \\" + "\n")
            out.append(r"\bottomrule\end{tabular}\end{minipage}\par" + "\n")
    assert displayed == 19
    (PAPER / "appendices/carpet-tables.tex").write_text("".join(out))
    print(f"Packaged {len(paths)} files; rendered {displayed} checked derivations.")


if __name__ == "__main__":
    main()
