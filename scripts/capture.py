import argparse
import json
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", default="/dev/ttyACM0")
    p.add_argument("--out", required=True)
    p.add_argument("--duration", type=int, default=60)
    p.add_argument("--baud", type=int, default=115200)
    args = p.parse_args()
    try:
        import serial
    except ImportError:
        raise SystemExit("pyserial is not installed; pip install pyserial")
    end = time.time() + args.duration
    with serial.Serial(args.port, args.baud, timeout=1) as ser, open(args.out, "w") as out:
        out.write("ts_ms,temp_c,vcc_v,tx_bias_ma,rx_dbm,grade\n")
        while time.time() < end:
            raw = ser.readline().decode("utf-8", errors="replace").strip()
            if not raw.startswith("{"):
                continue
            rec = json.loads(raw)
            out.write(
                f"{rec['ts_ms']},{rec['temp_c']},{rec['vcc_v']},"
                f"{rec['tx_bias_ma']},{rec['rx_dbm']},{rec['grade']}\n"
            )


if __name__ == "__main__":
    main()
