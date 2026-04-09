"""模拟引擎 - 串联 Agent / Device / Network 运行闭环"""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from .config import SimulationConfig
from .device import PhysicalDevice
from .network import OpenCoinNetwork
from .agent import AIAgent


@dataclass
class SimulationResult:
    """模拟结果"""
    cycles: int
    network_status: dict
    agents_status: list
    devices_status: list
    history: list

    def summary(self) -> str:
        lines = [
            "=" * 56,
            " 📊 OpenCoin 模拟结果",
            "=" * 56,
            f" 总轮数: {self.cycles}",
            f" 初始供应量: {self.network_status['initial_supply']:,.0f}",
            f" 剩余供应量: {self.network_status['current_supply']:,.2f}",
            f" 累计销毁: {self.network_status['total_burned']:,.2f} "
            f"({self.network_status['burn_pct']:.4f}%)",
            f" 交易笔数: {self.network_status['transactions']}",
            "-" * 56,
        ]
        for a in self.agents_status:
            lines.append(
                f" 🤖 {a['name']} | 余额: {a['balance']:,.2f} | "
                f"认知: {a['cognitive_level']:.2f} | "
                f"完成: {a['completed']} 失败: {a['failed']}"
            )
        lines.append("-" * 56)
        for d in self.devices_status:
            status = "💀 报废" if not d["alive"] else f"健康 {d['health']*100:.1f}%"
            lines.append(
                f" ⚙️  {d['name']} | 磨损: {d['wear']:.1f}% | "
                f"执行: {d['actions']} | {status}"
            )
        lines.append("=" * 56)
        return "\n".join(lines)


class Simulator:
    """OpenCoin 闭环模拟器"""

    def __init__(self, config: SimulationConfig | None = None):
        self.config = config or SimulationConfig()
        self.network = OpenCoinNetwork(config=self.config.network)
        self.agents: list[AIAgent] = []
        self.devices: list[PhysicalDevice] = []
        self.history: list[dict] = []
        self.cycle = 0

    def add_agent(self, name: str) -> AIAgent:
        agent = AIAgent(name=name, config=self.config.agent)
        self.agents.append(agent)
        return agent

    def add_device(self, name: str, precision: float = 1.0) -> PhysicalDevice:
        device = PhysicalDevice(name=name, precision=precision,
                                config=self.config.device)
        self.devices.append(device)
        return device

    def step(self) -> list[dict]:
        """执行一轮模拟：每个 Agent 尝试调用每个活着的 Device"""
        self.cycle += 1
        results = []

        for agent in self.agents:
            for device in self.devices:
                if not device.is_alive:
                    continue
                if not agent.can_afford(device):
                    continue

                result = agent.request_action(device, self.network, self.cycle)
                if result:
                    results.append(result)

        self.history.extend(results)
        return results

    def run(self, verbose: bool = True) -> SimulationResult:
        """运行完整模拟"""
        if verbose:
            print("\n" + "=" * 56)
            print(" 🚀 OpenCoin 物理工作量证明 (PoPW) 引擎启动")
            print("=" * 56)
            for a in self.agents:
                print(f" 🤖 Agent: {a.name} | 初始余额: {a.coins:,.0f}")
            for d in self.devices:
                print(f" ⚙️  Device: {d.name} | 精度: {d.precision}x")
            print("-" * 56)

        while True:
            # 检查是否所有设备报废
            if all(not d.is_alive for d in self.devices):
                if verbose:
                    print(f"\n ⚠️  所有设备已报废，模拟结束")
                break

            # 检查所有 Agent 是否都付不起任何设备
            if all(
                not any(agent.can_afford(d) for d in self.devices if d.is_alive)
                for agent in self.agents
            ):
                if verbose:
                    print(f"\n ❌ 所有 Agent 余额耗尽，模拟结束")
                break

            # 最大轮数限制
            if self.config.max_cycles > 0 and self.cycle >= self.config.max_cycles:
                if verbose:
                    print(f"\n ⏹️  达到最大轮数 ({self.config.max_cycles})，模拟结束")
                break

            results = self.step()

            if verbose:
                ns = self.network.status()
                print(
                    f"\n[ 区块 #{self.cycle} ] "
                    f"供应量: {ns['current_supply']:,.2f} | "
                    f"销毁: {ns['total_burned']:,.2f}"
                )
                for r in results:
                    print(
                        f"  ├─ {r['cost']:.1f} 支付 → "
                        f"销毁 {r['burned']:.1f} | "
                        f"磨损 {r['device_wear']:.1f}% | "
                        f"认知 {r['cognitive_level']:.2f}"
                    )

            if self.config.tick_delay > 0:
                time.sleep(self.config.tick_delay)

        return SimulationResult(
            cycles=self.cycle,
            network_status=self.network.status(),
            agents_status=[a.status() for a in self.agents],
            devices_status=[d.status() for d in self.devices],
            history=self.history,
        )
