import subprocess
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, asin, pi
import csv

S_exact = 0.25 * pi + 1.25 * asin(0.8) - 1


circles = f"1 1 1  1.5 2 {sqrt(5)/2}  2 1.5 {sqrt(5)/2}"
wide = (0, 3, 0, 3)
r = sqrt(5) / 2
tight = (2 - r, 2, 2 - r, 2)


def run_cpp(N, rect):
    xmin, xmax, ymin, ymax = rect
    inp = f"{circles} {N} {xmin} {xmax} {ymin} {ymax}\n"

    result = subprocess.run(
        ["./mc"],
        input=inp.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout.decode().strip())


Ns = list(range(100, 100001, 500))


wide_vals, tight_vals = [], []
wide_errs, tight_errs = [], []
rows = []


for N in Ns:
    Sw = run_cpp(N, wide)
    St = run_cpp(N, tight)

    Ew = abs(Sw - S_exact) / S_exact * 100
    Et = abs(St - S_exact) / S_exact * 100

    wide_vals.append(Sw)
    tight_vals.append(St)
    wide_errs.append(Ew)
    tight_errs.append(Et)

    rows.append([N, Sw, St, Ew, Et])



with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["N", "area_wide", "area_tight", "err_wide_%", "err_tight_%"])
    writer.writerows(rows)


plt.figure(figsize=(12,6))
plt.plot(Ns, wide_vals, label="Широкая область", color="blue")
plt.plot(Ns, tight_vals, label="Узкая область", color="orange")
plt.axhline(S_exact, color='black', linestyle='--', label="Точная площадь")

plt.xlabel("Количество точек N")
plt.ylabel("Оценка площади")
plt.title("График типа 1 — S(N)")
plt.grid(True)
plt.legend()
plt.savefig("plot_area.png", dpi=200)


plt.figure(figsize=(12,6))
plt.plot(Ns, wide_errs, label="Широкая область", color="blue")
plt.plot(Ns, tight_errs, label="Узкая область", color="orange")

plt.xlabel("Количество точек N")
plt.ylabel("Отклонение (%)")
plt.title("График типа 2 — error(N)")
plt.grid(True)
plt.legend()
plt.savefig("plot_error.png", dpi=200)

