"""
Simple Trust & Reputation System

- Providers have hidden true_quality in [0,1].
- Clients interact with providers and provide binary feedback (1=positive, 0=negative).
- Each client keeps per-provider feedback counts.
- Per-client trust score for provider p: (pos + 1) / (pos + neg + 2)  (Beta(1,1) prior -> Laplace smoothing)
- Provider reputation: mean of all clients' trust scores for that provider.
- Clients choose provider with highest reputation when selecting.
"""

import random
from collections import defaultdict
from typing import Dict, List, Tuple

random.seed(123)  # reproducible demo


class Provider:
    def __init__(self, pid: int, true_quality: float):
        self.id = pid
        self.true_quality = float(true_quality)  # probability of delivering positive experience
        self.global_pos = 0
        self.global_neg = 0

    def deliver_service(self) -> int:
        """Return 1 for positive experience, 0 for negative (stochastic using true_quality)."""
        return 1 if random.random() < self.true_quality else 0


class Client:
    def __init__(self, cid: int):
        self.id = cid
        self.feedback_counts: Dict[int, List[int]] = defaultdict(lambda: [0, 0])

    def give_feedback(self, provider: Provider, outcome: int):
        """Record client feedback for provider (outcome=1 or 0)"""
        if outcome == 1:
            self.feedback_counts[provider.id][0] += 1
            provider.global_pos += 1
        else:
            self.feedback_counts[provider.id][1] += 1
            provider.global_neg += 1

    def trust_score_for(self, provider_id: int) -> float:
        """Compute per-client trust estimate for a provider with Laplace smoothing."""
        pos, neg = self.feedback_counts.get(provider_id, [0, 0])
        return (pos + 1) / (pos + neg + 2)  # Beta(1,1) posterior mean


class TrustReputationSystem:
    def __init__(self):
        self.providers: Dict[int, Provider] = {}
        self.clients: Dict[int, Client] = {}

    def add_provider(self, pid: int, true_quality: float):
        self.providers[pid] = Provider(pid, true_quality)

    def add_client(self, cid: int):
        self.clients[cid] = Client(cid)

    def run_interaction(self, client: Client, provider: Provider):
        """One interaction: service delivered, client records feedback."""
        outcome = provider.deliver_service()
        client.give_feedback(provider, outcome)

    def compute_reputation(self, provider_id: int) -> float:
        """Aggregate reputation as mean of all clients' trust scores for this provider."""
        if not self.clients:
            return 0.0
        scores = [client.trust_score_for(provider_id) for client in self.clients.values()]
        return sum(scores) / len(scores)

    def select_best_provider(self) -> Tuple[int, float]:
        """Select provider with highest reputation; return (pid, reputation)."""
        best_pid, best_rep = None, -1.0
        for pid in self.providers:
            rep = self.compute_reputation(pid)
            if rep > best_rep:
                best_pid, best_rep = pid, rep
        return best_pid, best_rep

    def simulate(self, rounds: int, interactions_per_round: int = 1):
        """Each round: each client selects a provider (by current reputation) and interacts."""
        for r in range(1, rounds + 1):
            client_ids = list(self.clients.keys())
            random.shuffle(client_ids)
            for cid in client_ids:
                client = self.clients[cid]
                best_pid, _ = self.select_best_provider()
                if best_pid is None:
                    best_pid = random.choice(list(self.providers.keys()))
                provider = self.providers[best_pid]
                for _ in range(interactions_per_round):
                    self.run_interaction(client, provider)

    def print_status(self):
        print("=== Providers summary ===")
        for pid, prov in self.providers.items():
            rep = self.compute_reputation(pid)
            print(f"Provider {pid}: true_quality={prov.true_quality:.3f}, global_pos={prov.global_pos}, global_neg={prov.global_neg}, reputation={rep:.4f}")
            print("   Per-client trust scores:")
            for cid, client in self.clients.items():
                t = client.trust_score_for(pid)
                print(f"      Client {cid}: trust={t:.4f}  (pos,neg)={client.feedback_counts.get(pid, [0,0])}")
        best_pid, best_rep = self.select_best_provider()
        if best_pid is not None:
            print(f"\nSelected best provider by reputation: Provider {best_pid} with reputation {best_rep:.4f}")
        else:
            print("\nNo providers available.")


def demo():
    # create system
    sys = TrustReputationSystem()

    # Add providers (id, true_quality)
    sys.add_provider(1, 0.85)   # high-quality provider
    sys.add_provider(2, 0.60)   # medium-quality
    sys.add_provider(3, 0.35)   # low-quality

    # Add clients
    num_clients = 8
    for cid in range(1, num_clients + 1):
        sys.add_client(cid)

    # Initial state print (no interactions)
    print("Initial state (no interactions):")
    sys.print_status()
    print("\n--- Running simulation: clients pick best provider by current reputation and interact ---\n")

    # Run simulation: many rounds so reputations converge
    sys.simulate(rounds=30, interactions_per_round=1)

    # Final status
    print("\nFinal status after simulation:")
    sys.print_status()

    # Show some extra summary
    print("\nDetailed provider reputations (rounded):")
    for pid in sys.providers:
        print(f" Provider {pid}: Reputation = {sys.compute_reputation(pid):.3f}")


if __name__ == "__main__":
    demo()
