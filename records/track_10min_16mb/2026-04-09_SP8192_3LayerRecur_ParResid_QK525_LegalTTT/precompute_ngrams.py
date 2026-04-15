"""
Precompute n-gram "possible next token" masks from training shards.

For each n-gram context, records which next tokens were ever observed.
Tokens that were NEVER observed after a given context are "impossible"
and will be penalized during training.

Outputs (saved to DATA_DIR):
  bigram_possible_sp{V}.pt          [V, V] bool
  trigram_possible_sp{V}_k{K}.pt    [K, V] bool
  trigram_lookup_sp{V}_k{K}.pt      [V, V] int32  (-1 = not in top-K)

Usage:
  DATA_DIR=/path/to/data python3 precompute_ngrams.py
"""
import glob, os, numpy as np, torch
from pathlib import Path

VOCAB   = int(os.environ.get('VOCAB_SIZE',   8192))
K       = int(os.environ.get('NGRAM_TRIGRAM_K', 16384))
DATA_DIR = os.environ.get('DATA_DIR', './data/')
HEADER_BYTES = 256 * 4

files = sorted(glob.glob(
    os.path.join(DATA_DIR, 'datasets', f'fineweb10B_sp{VOCAB}', 'fineweb_train_*.bin')))
if not files:
    raise FileNotFoundError(f'No training shards found under {DATA_DIR}')

print(f'Building n-gram possible masks  vocab={VOCAB}  trigram_K={K}  shards={len(files)}')

# ---------------------------------------------------------------------------
# Pass 1 — bigram possible mask  +  trigram context occurrence counts
# ---------------------------------------------------------------------------
bigram_possible     = np.zeros((VOCAB, VOCAB), dtype=np.bool_)
trigram_ctx_counts  = np.zeros(VOCAB * VOCAB,  dtype=np.int64)

for f in files:
    n  = int(np.fromfile(f, dtype='<i4', count=256)[2])
    mm = np.memmap(f, mode='r', dtype='<u2', offset=HEADER_BYTES, shape=(n,))
    t  = mm.astype(np.int32)

    # bigram: mark every observed (prev, next) pair
    bigram_possible.reshape(-1)[
        t[:-1].astype(np.int64) * VOCAB + t[1:].astype(np.int64)] = True

    # trigram context frequency: how often does each (prev2, prev1) pair appear
    ctx = t[:-2].astype(np.int64) * VOCAB + t[1:-1].astype(np.int64)
    np.add.at(trigram_ctx_counts, ctx, 1)

    print(f'  pass1  {Path(f).name}  {n:,} tokens')

# top-K trigram contexts by occurrence count
top_k_flat = np.argpartition(trigram_ctx_counts, -K)[-K:]
top_k_flat = top_k_flat[np.argsort(trigram_ctx_counts[top_k_flat])[::-1]]

trigram_lookup_flat = np.full(VOCAB * VOCAB, -1, dtype=np.int32)
for row_idx, ctx_flat in enumerate(top_k_flat):
    trigram_lookup_flat[ctx_flat] = row_idx

# ---------------------------------------------------------------------------
# Pass 2 — trigram possible masks for top-K contexts
# ---------------------------------------------------------------------------
trigram_possible = np.zeros((K, VOCAB), dtype=np.bool_)

for f in files:
    n  = int(np.fromfile(f, dtype='<i4', count=256)[2])
    mm = np.memmap(f, mode='r', dtype='<u2', offset=HEADER_BYTES, shape=(n,))
    t  = mm.astype(np.int32)

    ctx         = t[:-2].astype(np.int64) * VOCAB + t[1:-1].astype(np.int64)
    row_indices = trigram_lookup_flat[ctx]          # -1 where not in top-K
    valid       = row_indices >= 0
    rows        = row_indices[valid].astype(np.int64)
    nexts       = t[2:][valid].astype(np.int64)

    trigram_possible.reshape(-1)[rows * VOCAB + nexts] = True
    print(f'  pass2  {Path(f).name}')

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out = {
    f'bigram_possible_sp{VOCAB}.pt':
        (torch.from_numpy(bigram_possible), bigram_possible),
    f'trigram_possible_sp{VOCAB}_k{K}.pt':
        (torch.from_numpy(trigram_possible), trigram_possible),
    f'trigram_lookup_sp{VOCAB}_k{K}.pt':
        (torch.from_numpy(trigram_lookup_flat.reshape(VOCAB, VOCAB)), None),
}
for fname, (tensor, arr) in out.items():
    path = os.path.join(DATA_DIR, fname)
    torch.save(tensor, path)
    info = f'{tuple(tensor.shape)} {tensor.dtype}'
    if arr is not None:
        pct = 100.0 * arr.mean()
        info += f'  possible={pct:.1f}%  impossible={100-pct:.1f}%'
    print(f'saved  {path}  {info}')
