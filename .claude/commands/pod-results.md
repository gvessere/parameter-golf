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
   - Check if experiments/baseline points to an existing experiment directory (contains the path to the baseline)
   - If no baseline file exists, list available experiments and ask the user which to use as baseline (or confirm there is none)
   - Extract the baseline's final val loss from its train.log

6. Write a conclusion in meta.md:
   - If no baseline: "No baseline available for comparison."
   - If baseline exists: state which experiment is the baseline, its val loss, the delta (e.g. "+0.012 worse" or "-0.008 better"), and a one-line verdict: "better", "worse", or "close" (within 0.005 = close)

7. Print a summary: directory created, final val loss, comparison to baseline, git hash.

8. Offer to commit the new experiment directory to git. Also ask if this run should become the new baseline (updates experiments/baseline).
