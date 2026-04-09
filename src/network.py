"""代币网络模块 - 模拟 OpenCoin 智能合约结算层"""

from dataclasses import dataclass, field
from .config import NetworkConfig


@dataclass
class Transaction:
    """单笔交易记录"""
    cycle: int
    agent_name: str
    device_name: str
    amount: float
    burned: float
    remaining_supply: float


@dataclass
class OpenCoinNetwork:
    """OpenCoin 代币网络"""
    config: NetworkConfig = field(default_factory=NetworkConfig)
    total_supply: float = 0.0
    total_burned: float = 0.0
    total_transactions: int = 0
    ledger: list = field(default_factory=list)

    def __post_init__(self):
        self.total_supply = self.config.initial_supply

    def process_transaction(self, amount: float, cycle: int,
                            agent_name: str, device_name: str) -> Transaction:
        """处理一笔交易：扣减供应量，执行销毁"""
        burn_amount = amount * self.config.burn_rate
        self.total_supply -= burn_amount
        self.total_burned += burn_amount
        self.total_transactions += 1

        tx = Transaction(
            cycle=cycle,
            agent_name=agent_name,
            device_name=device_name,
            amount=amount,
            burned=burn_amount,
            remaining_supply=self.total_supply,
        )
        self.ledger.append(tx)
        return tx

    @property
    def burn_percentage(self) -> float:
        """已销毁占初始供应量的比例"""
        if self.config.initial_supply == 0:
            return 0.0
        return self.total_burned / self.config.initial_supply

    def status(self) -> dict:
        return {
            "initial_supply": self.config.initial_supply,
            "current_supply": round(self.total_supply, 2),
            "total_burned": round(self.total_burned, 2),
            "burn_pct": round(self.burn_percentage * 100, 4),
            "transactions": self.total_transactions,
        }
