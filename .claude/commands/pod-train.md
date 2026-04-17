Execute the parameter-golf training script on the RunPod pod in a tmux session.

Arguments: `$ARGUMENTS` should contain `host port` (e.g. `213.173.108.12 19020`). If not provided, query the RunPod API for the running pod's SSH details.

Kill any existing tmux 'train' session, then run these steps before starting training:

```
cd /workspace/parameter-golf
git pull
cp records/track_10min_16mb/2026-04-09_SP8192_3LayerRecur_ParResid_QK525_LegalTTT/* /workspace/parameter-golf/
```

Then start the training session:

```
cd /workspace/parameter-golf
SKIP_QUANTIZATION=1 \
MARS_WEIGHT=1.0 MARS_BLOCK_SIZE=4 \
MULTI_STEP_WEIGHT=0.0 TOKEN_DROPOUT_RATE=0.0 \
ITERATIONS=2000 MAX_WALLCLOCK_SECONDS=99999 \
VAL_LOSS_EVERY=500 \
DATA_DIR=/workspace/parameter-golf/data \
SEED=42 QK_GAIN_INIT=5.25 \
TTT_ENABLED=1 TTT_LR=0.005 TTT_EPOCHS=3 \
TRAIN_BATCH_TOKENS=131070 \
torchrun --standalone --nproc_per_node=1 train_gpt.py 2>&1 | tee /workspace/train.log
```

After starting, wait 20 seconds and tail /workspace/train.log to verify the run started correctly. Confirm mars_weight and mars_block_size appear in the log.

## Comparison target
- **Quality**: pre-quantization val_loss target ~2.809 (8-GPU baseline mean, with batch size advantage)
- **Throughput**: target ~120k tokens/s (baseline on 8×GPU). Current single-GPU throughput will be lower — note it from `tok/s` in the log. Optimize for throughput only after quality is validated.
