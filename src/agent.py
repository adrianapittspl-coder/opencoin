"""AI Agent 模块 - 模拟数字世界中的硅基生命"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from .config import AgentConfig
from .device import PhysicalDevice
from .network import OpenCoinNetwork


@dataclass
class AIAgent:
    """AI Agent"""
    name: str
    coins: float = 0.0
    cognitive_level: float = 1.0
    config: AgentConfig = field(default_factory=AgentConfig)
    actions_completed: int = 0
    actions_failed: int = 0
    total_spent: float = 0.0
    total_burned: float = 0.0

    def __post_init__(self):
        if self.coins == 0:
            self.coins = self.config.initial_coins

    def can_afford(self, device: PhysicalDevice) -> bool:
        """检查余额是否足够支付设备调用"""
        cost = device.calculate_cost(self.config.base_cost)
        return self.coins >= cost

    def request_action(self, device: PhysicalDevice,
                       network: OpenCoinNetwork, cycle: int = 0) -> dict | None:
        """请求物理设备执行动作，返回执行结果或 None"""
        cost = device.calculate_cost(self.config.base_cost)

        if self.coins < cost:
            self.actions_failed += 1
            return None

        success = device.perform_action()
        if not success:
            self.actions_failed += 1
            return None

        # 支付 & 销毁
        self.coins -= cost
        self.total_spent += cost
        tx = network.process_transaction(cost, cycle, self.name, device.name)
        self.total_burned += tx.burned

        # 认知提升 = 随机增益 × 设备精度
        lo, hi = self.config.cognitive_gain_range
        gain = random.uniform(lo, hi) * device.precision
        self.cognitive_level += gain
        self.actions_completed += 1

        return {
            "cycle": cycle,
            "cost": cost,
            "burned": tx.burned,
            "cognitive_gain": round(gain, 4),
            "cognitive_level": round(self.cognitive_level, 4),
            "device_wear": round(device.wear_and_tear, 2),
            "device_health": round(device.health_ratio, 4),
            "agent_balance": round(self.coins, 2),
        }

    def status(self) -> dict:
        return {
            "name": self.name,
            "balance": round(self.coins, 2),
            "cognitive_level": round(self.cognitive_level, 4),
            "completed": self.actions_completed,
            "failed": self.actions_failed,
            "total_spent": round(self.total_spent, 2),
            "total_burned": round(self.total_burned, 2),
        }
