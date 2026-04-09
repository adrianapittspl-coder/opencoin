"""物理设备模块 - 模拟现实世界中的物理接口"""

import random
from dataclasses import dataclass, field
from .config import DeviceConfig


@dataclass
class PhysicalDevice:
    """物理设备（机械臂、无人机、传感器等）"""
    name: str
    precision: float = 1.0
    config: DeviceConfig = field(default_factory=DeviceConfig)
    wear_and_tear: float = 0.0
    actions_performed: int = 0
    is_alive: bool = True

    @property
    def remaining_life(self) -> float:
        """剩余寿命百分比"""
        return max(0.0, self.config.max_wear - self.wear_and_tear)

    @property
    def health_ratio(self) -> float:
        """健康度 (1.0=全新, 0.0=报废)"""
        return max(0.0, 1.0 - self.wear_and_tear / self.config.max_wear)

    def perform_action(self) -> bool:
        """执行物理动作，返回是否成功"""
        if not self.is_alive:
            return False

        if self.wear_and_tear >= self.config.max_wear:
            self.is_alive = False
            return False

        # 磨损 = 基础随机值 × 精度系数
        lo, hi = self.config.base_wear
        wear_increase = random.uniform(lo, hi) * self.precision
        self.wear_and_tear = min(self.config.max_wear, self.wear_and_tear + wear_increase)
        self.actions_performed += 1

        if self.wear_and_tear >= self.config.max_wear:
            self.is_alive = False

        return True

    def calculate_cost(self, base_cost: float) -> float:
        """计算调用费用 = 基础费用 × 精度系数"""
        return base_cost * self.precision

    def status(self) -> dict:
        """返回设备状态快照"""
        return {
            "name": self.name,
            "precision": self.precision,
            "wear": round(self.wear_and_tear, 2),
            "health": round(self.health_ratio, 4),
            "actions": self.actions_performed,
            "alive": self.is_alive,
        }
