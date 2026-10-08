import argparse
import numpy as np


def load_csv(path):
    rows = []
    with open(path) as f:
        header = f.readline().strip().split(",")
        idx = [header.index(c) for c in ("temp_c", "vcc_v", "tx_bias_ma", "rx_dbm")]
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 5:
                continue
            rows.append([float(parts[i]) for i in idx])
    return np.asarray(rows, dtype=np.float64)


def train(x, steps, lr):
    rng = np.random.default_rng(1)
    w1 = rng.normal(scale=0.1, size=(4, 2))
    b1 = np.zeros(2)
    w2 = rng.normal(scale=0.1, size=(2, 4))
    b2 = np.zeros(4)
    for step in range(steps):
        z = x @ w1 + b1
        h = np.maximum(z, 0)
        y = h @ w2 + b2
        err = y - x
        dw2 = h.T @ err / len(x)
        db2 = err.mean(axis=0)
        dh = err @ w2.T
        dz = dh * (z > 0)
        dw1 = x.T @ dz / len(x)
        db1 = dz.mean(axis=0)
        w1 -= lr * dw1
        b1 -= lr * db1
        w2 -= lr * dw2
        b2 -= lr * db2
        if step % 200 == 0:
            mse = float((err ** 2).mean())
            print(f"step {step} train_mse {mse:.6f}")
    return w1, b1, w2, b2


def emit(path, mean, scale, w1, b1, w2, b2):
    def arr(name, a):
        flat = ", ".join(f"{v:.8f}f" for v in a.reshape(-1))
        return f"static const float {name}[{a.size}] = {{ {flat} }};\n"

    text = (
        "#ifndef AOPM_AE_WEIGHTS_H\n#define AOPM_AE_WEIGHTS_H\n"
        + arr("aopm_ae_mean", mean)
        + arr("aopm_ae_scale", scale)
        + arr("aopm_ae_w1", w1)
        + arr("aopm_ae_b1", b1)
        + arr("aopm_ae_w2", w2)
        + arr("aopm_ae_b2", b2)
        + "#endif\n"
    )
    with open(path, "w") as f:
        f.write(text)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--steps", type=int, default=800)
    args = p.parse_args()
    data = load_csv(args.csv)
    if len(data) < 10:
        raise SystemExit("need at least 10 rows")
    cut = int(len(data) * 0.8)
    train_x, val_x = data[:cut], data[cut:]
    mean = train_x.mean(axis=0)
    scale = train_x.std(axis=0)
    scale[scale < 1e-6] = 1.0
    w1, b1, w2, b2 = train((train_x - mean) / scale, args.steps, 0.05)
    val_z = (val_x - mean) / scale
    h = np.maximum(val_z @ w1 + b1, 0)
    y = h @ w2 + b2
    print(f"val_mse {float(((y - val_z) ** 2).mean()):.6f} rows {len(data)}")
    emit(args.out, mean, scale, w1, b1, w2, b2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
