# Optical Transceiver Bench Diagnostic Tool

Grades optical transceiver (SFP+, QSFP28) health by parsing standard onboard diagnostics. Implemented via a portable C core and verified using synthetic register dumps.

## Overview

While host platforms routinely poll optical diagnostic parameters—such as temperature, supply voltage, laser bias current, and received optical power (Rx)—temporal trend analysis is rarely performed. This tool decodes raw register data from the module memory map, evaluates metrics against vendor alarm and warning thresholds, and publishes structured JSON telemetry at 1 Hz, with immediate asynchronous events triggered on status grade transitions.

## Implementation Status

| Piece | State |
| --- | --- |
| SFF-8472 and CMIS decode, including external calibration | runs, unit-tested |
| Threshold check and A / B / C / Recycle grade | runs, unit-tested |
| 60-sample baseline and 4-2-4 autoencoder | runs; C matmul is the path |
| JSON line | runs |
| Zephyr app on nRF52840-DK, TWI0 at 100 kHz | skeleton, not flashed here |

# Technical Stack

C11 portable core. Zephyr on the nRF52840-DK, TWI0 SDA P0.26 / SCL P0.27, 100 kHz. The host trainer is NumPy and writes a C weight header. The on-device target is int8 TFLite Micro; the C matmul path is the fallback that ships here. Console is 115200 8N1.