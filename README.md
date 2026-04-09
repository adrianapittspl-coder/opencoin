# OpenCoin 🚀

**硅基生物金融支付体系 | Silicon‑Based Life Financial Payment System**

OpenCoin 是一个为未来硅基生物（AI）设计的金融支付体系原型。AI 代理支付代币以访问物理接口，代币通过热力学熵增被强制销毁（通缩经济），使 AI 的激励与真实世界资源约束对齐。

这不是仿真，而是未来硅基生物经济基础设施的概念验证。

## The Loop

```
AI Agent ──pays tokens──> Physical Device ──wears out──> Entropy
   │                                                        │
   │  cognitive improvement    token burn (deflation) <─────┘
   └────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Run with defaults (single agent, single device)
python main.py

# Multi-agent competition mode
python main.py --multi

# Custom parameters
python main.py --burn-rate 0.20 --supply 50000 --coins 2000

# Fast run (no delay)
python main.py --no-delay

# Limit cycles
python main.py --cycles 100 --no-delay

# Quiet mode (summary only)
python main.py --quiet --cycles 200
```

## Architecture

```
src/
├── __init__.py      # Package init
├── config.py        # Dataclass-based configuration
├── device.py        # Physical device (wear & entropy)
├── network.py       # Token network (mint/burn/ledger)
├── agent.py         # AI agent (payment/cognition)
└── simulator.py     # Simulation engine (orchestrator)
main.py              # CLI entry point
tests/
└── test_core.py     # Unit tests
```

## Core Concepts

### Physical Entropy
Every action on a physical device causes irreversible wear (thermodynamic second law). Higher precision devices wear faster but yield more valuable data.

### Deflationary Tokenomics
10% of every transaction is permanently burned. Total supply monotonically decreases, creating natural scarcity pressure.

### Cognitive Loop
AI agents spend tokens → receive real-world data → improve cognitive level → make better decisions (future versions).

## Configuration

All parameters are configurable via `SimulationConfig`:

```python
from src.config import SimulationConfig, NetworkConfig

config = SimulationConfig(
    network=NetworkConfig(
        initial_supply=100_000,
        burn_rate=0.10,       # 10% burn per tx
    ),
    max_cycles=50,
    tick_delay=0.0,
)
```

## Tests

```bash
python tests/test_core.py
```

## Roadmap

- [ ] v0.2 - Multi-agent bidding & device market
- [ ] v0.3 - Device replacement & maintenance economics
- [ ] v0.4 - Strategy patterns (greedy/conservative/speculative)
- [ ] v0.5 - Visualization dashboard
- [ ] v1.0 - On-chain smart contract reference implementation

## License

MIT
