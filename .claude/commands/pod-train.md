Execute the parameter-golf training script on the RunPod pod in a tmux session.

Arguments: `$ARGUMENTS` should contain the full env var string to pass to the training command (e.g. `"MARS_WEIGHT=0.1 MARS_MASK_RATE=0.15"`). If not provided, ask the user for the experiment parameters. Host/port are inferred from the RunPod API if not known.

Kill any existing tmux 'train' session, then run these steps before starting training:

```
cd /workspace/parameter-golf
git pull
cp records/track_10min_16mb/2026-04-09_SP8192_3LayerRecur_ParResid_QK525_LegalTTT/* /workspace/parameter-golf/
```

Then start the training session with the fixed infrastructure params plus the experiment-specific env vars from $ARGUMENTS:

```
cd /workspace/parameter-golf
SKIP_QUANTIZATION=1 \
ITERATIONS=2000 MAX_WALLCLOCK_SECONDS=99999 \
VAL_LOSS_EVERY=500 \
DATA_DIR=/workspace/parameter-golf/data \
SEED=42 QK_GAIN_INIT=5.25 \
TTT_ENABLED=1 TTT_LR=0.005 TTT_EPOCHS=3 \
TRAIN_BATCH_TOKENS=131070 \
<experiment env vars from $ARGUMENTS> \
torchrun --standalone --nproc_per_node=1 train_gpt.py 2>&1 | tee /workspace/train.log
```

After starting, wait 20 seconds and tail /workspace/train.log to verify the run started correctly.
