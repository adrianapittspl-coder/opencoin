#!/usr/bin/env python3
"""OpenCoin - 物理工作量证明模拟引擎

用法:
    python main.py                    # 默认单设备单Agent
    python main.py --multi            # 多设备多Agent竞争
    python main.py --cycles 50        # 限制最大轮数
    python main.py --burn-rate 0.20   # 自定义销毁比例
    python main.py --no-delay         # 无延迟运行
"""

import argparse
from src.config import SimulationConfig, NetworkConfig, DeviceConfig, AgentConfig
from src.simulator import Simulator


def single_scenario(config: SimulationConfig) -> Simulator:
    """单Agent单设备场景"""
    sim = Simulator(config)
    sim.add_agent("Vision-AI-01")
    sim.add_device("高精度合成生物舱", precision=3.0)
    return sim


def multi_scenario(config: SimulationConfig) -> Simulator:
    """多Agent多设备竞争场景"""
    sim = Simulator(config)
    sim.add_agent("Alpha-AI")
    sim.add_agent("Beta-AI")
    sim.add_device("机械臂-A", precision=2.0)
    sim.add_device("传感器阵列-B", precision=1.5)
    sim.add_device("无人机集群-C", precision=4.0)
    return sim


def main():
    parser = argparse.ArgumentParser(description="OpenCoin PoPW 模拟引擎")
    parser.add_argument("--multi", action="store_true", help="多设备多Agent竞争模式")
    parser.add_argument("--cycles", type=int, default=0, help="最大轮数 (0=无限)")
    parser.add_argument("--burn-rate", type=float, default=0.10, help="销毁比例 (0-1)")
    parser.add_argument("--supply", type=float, default=100000, help="初始供应量")
    parser.add_argument("--coins", type=float, default=1000, help="Agent初始余额")
    parser.add_argument("--base-cost", type=float, default=20, help="基础调用费用")
    parser.add_argument("--delay", type=float, default=0.5, help="每轮延迟秒数")
    parser.add_argument("--no-delay", action="store_true", help="无延迟运行")
    parser.add_argument("--quiet", action="store_true", help="静默模式")
    args = parser.parse_args()

    config = SimulationConfig(
        network=NetworkConfig(initial_supply=args.supply, burn_rate=args.burn_rate),
        agent=AgentConfig(initial_coins=args.coins, base_cost=args.base_cost),
        max_cycles=args.cycles,
        tick_delay=0.0 if args.no_delay else args.delay,
    )

    if args.multi:
        sim = multi_scenario(config)
    else:
        sim = single_scenario(config)

    result = sim.run(verbose=not args.quiet)
    print(result.summary())


if __name__ == "__main__":
    main()
