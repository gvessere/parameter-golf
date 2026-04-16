Prepare a RunPod pod for parameter-golf training. Requires SSH access via ~/.ssh/id_runpod.

Arguments: `$ARGUMENTS` should contain `host port` (e.g. `213.173.108.12 19020`). If not provided, query the RunPod API for the running pod's SSH details.

Steps to run via SSH (ssh -i ~/.ssh/id_runpod -o StrictHostKeyChecking=no root@<host> -p <port>):

1. If /workspace/parameter-golf/.git does not exist:
   - cd /workspace/parameter-golf
   - git init
   - git remote add origin https://github.com/gvessere/parameter-golf.git

2. git fetch origin graph_kl && git checkout -f graph_kl && git pull

3. pip install -r requirements.txt --break-system-packages -q

4. pip install brotli sentencepiece --break-system-packages -q

5. pip install flash_attn_3 --no-deps --find-links https://windreamer.github.io/flash-attention3-wheels/cu128_torch291/ --break-system-packages -q

6. If data not present (check /workspace/parameter-golf/data/datasets/fineweb10B_sp8192/):
   cd /workspace/parameter-golf && MATCHED_FINEWEB_REPO_ID=kevclark/parameter-golf python3 data/cached_challenge_fineweb.py --variant sp8192

7. cp records/track_10min_16mb/2026-04-09_SP8192_3LayerRecur_ParResid_QK525_LegalTTT/* /workspace/parameter-golf/

Print status after each step. Pod is ready when all steps complete.
