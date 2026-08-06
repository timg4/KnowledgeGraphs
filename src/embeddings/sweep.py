"""Multi-seed robustness sweep for the embedding experiment.

The single-seed cluster cross-check (LO12) turned out to be seed-sensitive on
this small graph (20 teams, 9.3k triples), so we report link-prediction metrics
and the style-cluster agreement as mean +/- spread across several seeds, against
a chance baseline computed from the actual cluster sizes.

Usage:  .venv-emb/Scripts/python -m src.embeddings.sweep
Writes: generated/embeddings/sweep.json
"""

import json

import numpy as np

from .train import (METRICS, OUT_DIR, TRIPLES, style_clusters, team_neighbours,
                    train)

SEEDS = [42, 1040, 7, 123, 2024, 99, 512, 2718]
MODELS = ("TransE", "ComplEx")
KEYS = ("mrr", "hits@1", "hits@3", "hits@10")


def chance_baseline(clusters, teams):
    """Expected same-cluster nearest neighbours if neighbours were random:
    sum over teams of (own cluster size - 1) / (N - 1)."""
    from collections import Counter
    sizes = Counter(clusters[t] for t in teams)
    n = len(teams)
    return sum((sizes[clusters[t]] - 1) / (n - 1) for t in teams)


def main():
    from pykeen.triples import TriplesFactory

    clusters = style_clusters()
    base_tf = TriplesFactory.from_path(str(TRIPLES))
    teams = [t for t in clusters if t in base_tf.entity_to_id]
    baseline = chance_baseline(clusters, teams)
    print(f"{base_tf.num_triples} triples, {len(teams)} teams · "
          f"chance same-cluster baseline = {baseline:.1f}/{len(teams)}\n")

    results = {m: {**{k: [] for k in KEYS}, "cluster": []} for m in MODELS}

    for seed in SEEDS:
        tf = TriplesFactory.from_path(str(TRIPLES))
        training, testing, validation = tf.split([0.8, 0.1, 0.1],
                                                 random_state=seed)
        for model_name in MODELS:
            res, metrics = train(model_name, training, validation, testing,
                                 seed=seed)
            nn = team_neighbours(res, tf, teams)
            agree = sum(clusters[t] == clusters[nn[t][0]] for t in teams)
            for k in KEYS:
                results[model_name][k].append(float(metrics[k]))
            results[model_name]["cluster"].append(agree)
            print(f"seed {seed:>4} {model_name:<8} "
                  + " ".join(f"{k}={metrics[k]:.3f}" for k in KEYS)
                  + f" cluster={agree}/{len(teams)}")

    print(f"\n{'':8} " + "  ".join(f"{k:>14}" for k in KEYS)
          + f"  {'cluster/'+str(len(teams)):>14}")
    summary = {"seeds": SEEDS, "n_teams": len(teams),
               "chance_cluster": baseline, "models": {}}
    for model_name in MODELS:
        row = results[model_name]
        cells = []
        stats = {}
        for k in KEYS:
            a = np.array(row[k])
            stats[k] = dict(mean=float(a.mean()), std=float(a.std()),
                            min=float(a.min()), max=float(a.max()))
            cells.append(f"{a.mean():.3f}+/-{a.std():.3f}")
        c = np.array(row["cluster"])
        stats["cluster"] = dict(mean=float(c.mean()), std=float(c.std()),
                                min=int(c.min()), max=int(c.max()))
        cells.append(f"{c.mean():.1f}+/-{c.std():.1f} [{c.min()}-{c.max()}]")
        summary["models"][model_name] = stats
        print(f"{model_name:<8} " + "  ".join(f"{x:>14}" for x in cells))

    (OUT_DIR / "sweep.json").write_text(json.dumps(summary, indent=2),
                                        encoding="utf-8")
    print(f"\n-> {OUT_DIR / 'sweep.json'}")


if __name__ == "__main__":
    main()
