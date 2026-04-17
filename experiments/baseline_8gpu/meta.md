# Baseline: 8-GPU official runs

**Important caveat**: these runs used 8 GPUs with a larger batch size. Direct val loss comparison to single-GPU runs is approximate — lower loss here partly reflects larger effective batch size, not just model quality.

## Results (pre-quantization, post-EMA)

| seed | val_loss | val_bpb |
|------|----------|---------|
| 42   | 2.80873  | 1.08735 |
| 314  | 2.80978  | 1.08775 |
| 999  | 2.81014  | 1.08789 |
| **mean** | **2.80955** | **1.08766** |

## Results (quantized + TTT sliding window)

| seed | val_loss | val_bpb |
|------|----------|---------|
| 42   | 2.79180  | 1.08079 |
| 314  | 2.79242  | 1.08103 |
| 999  | 2.79281  | 1.08118 |
| **mean** | **2.79234** | **1.08100** |
