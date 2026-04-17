Fetch training results from the RunPod pod and store them locally.

Arguments: `$ARGUMENTS` should contain a short description of the experiment (e.g. "mars 2L block4 weight1.0"). If not provided, ask the user for one.

Steps:

1. Get the git hash from the pod:
   ssh -i ~/.ssh/id_runpod root@<host> -p <port> "cd /workspace/parameter-golf && git rev-parse --short HEAD"
   If host/port not known, query the RunPod API for the running pod's SSH details.

2. Create a local directory:
   experiments/<YYYY-MM-DD>_<hash>/

3. Copy the log from the pod:
   scp -i ~/.ssh/id_runpod -P <port> root@<host>:/workspace/train.log experiments/<YYYY-MM-DD>_<hash>/train.log

4. Write experiments/<YYYY-MM-DD>_<hash>/meta.md with:
   - git hash (full)
   - short description from arguments
   - date/time
   - final val loss (grep the last "val_loss:" line from train.log)
   - key hyperparameters (grep the hyperparams block from train.log)

5. Determine the baseline for comparison:
   - Primary baseline: experiments/baseline_8gpu/meta.md — mean pre-quant val_loss: 2.80955, mean quantized+TTT val_loss: 2.79234. CAVEAT: these were 8-GPU runs with larger batch size, so they have an advantage. A single-GPU run matching or beating them is a strong result.
   - Secondary baseline: check if experiments/baseline points to a more recent single-GPU experiment to use as a closer comparison. If it exists, use that val_loss instead (or in addition).
   - Extract the current run's final val_loss from the last "pre-quantization post-ema val_loss:" line in train.log. If training didn't finish, use the last "val_loss:" line.

6. Write a conclusion in meta.md:
   - Compare to 8-GPU baseline mean (2.80955 pre-quant) and note the caveat
   - If secondary single-GPU baseline exists, compare to that too
   - Compute delta and verdict: "better" (delta < -0.002), "worse" (delta > +0.002), or "close" (within ±0.002)
   - One-line summary e.g.: "worse by 0.008 vs 8-GPU baseline (expected given 1 GPU); close to single-GPU baseline"

7. Print a summary: directory created, final val loss, comparison to baseline, git hash.

8. Offer to commit the new experiment directory to git. Also ask if this run should become the new single-GPU baseline (updates experiments/baseline file with the path).
