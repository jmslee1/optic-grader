# Detection

Normative inputs are SFF-8472 Rev 12.4 and CMIS 4.0.

## Features

| Feature | SFP+ (A2h) | QSFP28 | In the vector |
| --- | --- | --- | --- |
| Temperature | bytes 96–97, int16 / 256 °C | lower page 14–15, same scale | yes |
| Vcc | bytes 98–99, uint16 × 100 µV | lower page 16–17, same scale | yes |
| TX bias | bytes 100–101, uint16 × 2 µA | page 11h byte 170, lane 1 | yes |
| RX power | bytes 104–105, uint16 × 0.1 µW, then dBm | page 11h byte 186, lane 1 | yes |
| TX power | bytes 102–103, same optical scale | page 11h byte 154, lane 1 | reported only |

TX power tracks TX bias on a directly modulated laser, so a second copy of the same drift does not earn a feature slot. Lanes 2–4 are still emitted. The vector uses lane 1.

Thresholds come from the converted alarm and warning block, not from the flag bytes alone.

## Grades

| Grade | Rule |
| --- | --- |
| Recycle | No ACK, implausible identifier, or DDM unreadable. |
| C | Any alarm, LOS/LOL, or a Tier 3 anomaly held across the sustained window. |
| B | Warning only, or a Tier 3 anomaly that returned inside the window. |
| A | All four features nominal and Tier 3 stable. |

Tier 3 does not outrank an alarm. It can raise a nominal module to C only when the anomaly is held, and to B when it clears inside the window.