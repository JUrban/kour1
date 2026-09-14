#!/usr/bin/env python3
"""Render frozen CSV chronology as a standalone PGFPlots figure."""
import csv
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]


def main():
    def read(name):
        with (PAPER / "data" / name).open() as stream:
            return list(csv.DictReader(stream))
    commits = [r for r in read("research-commits.csv")
               if r["in_research_window"] == "True"]
    proofs = read("proof-artifact-timeline.csv")
    assert len(commits) == 198 and len(proofs) == 46
    def coordinates(rows):
        points = [(0., 0)] + [(float(r["elapsed_hours"]), i)
                             for i, r in enumerate(rows, 1)]
        assert all(0 <= x <= 48 for x, _ in points)
        points.append((48., len(rows)))
        return " ".join(f"({x:.9f},{y})" for x, y in points)
    source = r"""\documentclass[tikz,border=4pt]{standalone}
\usepackage{lmodern}
\usepackage{pgfplots}
\usepgfplotslibrary{groupplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
\begin{groupplot}[
 group style={group size=1 by 2,vertical sep=1.2cm},
 width=14.2cm,height=4.3cm,
 xmin=0,xmax=48,xtick={0,6,12,18,24,30,36,42,48},
 ymin=0,axis lines=left,grid=major,
 grid style={gray!18},tick label style={font=\small},
 label style={font=\small},title style={font=\small},
 enlargelimits=false]
\nextgroupplot[ymax=205,ytick={0,50,100,150,200},xticklabels=\empty,
 ylabel={Cumulative commits},
 title={Repository activity within the 48-hour window}]
\addplot[const plot,blue!65!black,line width=1pt] coordinates {
""" + coordinates(commits) + r"""};
\nextgroupplot[ymax=48,ytick={0,10,20,30,40,46},
 ylabel={Families with an artifact},
 xlabel={Hours since 10 September 2026, 20:56:46 UTC},
 title={First principal proof files for the 46 deadline candidate families}]
\addplot[const plot,orange!75!black,line width=1pt] coordinates {
""" + coordinates(proofs) + r"""};
\end{groupplot}
\end{tikzpicture}
\end{document}
"""
    folder = PAPER / "figures"
    folder.mkdir(exist_ok=True)
    (folder / "trajectory.tex").write_text(source)
    print("Generated figure source from 198 commits and 46 first-file observations.")


if __name__ == "__main__":
    main()
