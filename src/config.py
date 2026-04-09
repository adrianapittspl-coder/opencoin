"""OpenCoin Simulation Configuration"""

from dataclasses import dataclass, field


@dataclass
class NetworkConfig:
    """代币网络参数"""
    initial_supply: float = 100_000.0
    burn_rate: float = 0.10          # 每笔交易销毁比例 (0-1)
    min_burn_rate: float = 0.01      # 最低销毁比例
    max_burn_rate: float = 0.50      # 最高销毁比例


@dataclass
class DeviceConfig:
    """物理设备参数"""
    base_wear: tuple = (2.0, 5.0)    # 每次基础磨损范围
    max_wear: float = 100.0          # 报废阈值


@dataclass
class AgentConfig:
    """AI Agent 参数"""
    initial_coins: float = 1000.0
    base_cost: float = 20.0          # 基础调用费用
    cognitive_gain_range: tuple = (0.2, 0.8)  # 认知提升范围


@dataclass
class SimulationConfig:
    """总配置"""
    network: NetworkConfig = field(default_factory=NetworkConfig)
    device: DeviceConfig = field(default_factory=DeviceConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    tick_delay: float = 0.0          # 每轮延迟秒数, 0=无延迟
    max_cycles: int = 0              # 最大轮数, 0=无限(直到终止)
