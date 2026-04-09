"""OpenCoin 核心模块单元测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import SimulationConfig, NetworkConfig, DeviceConfig, AgentConfig
from src.device import PhysicalDevice
from src.network import OpenCoinNetwork
from src.agent import AIAgent
from src.simulator import Simulator


def test_device_wear():
    """设备磨损测试"""
    device = PhysicalDevice("测试设备", precision=1.0)
    assert device.is_alive
    assert device.wear_and_tear == 0.0
    assert device.health_ratio == 1.0

    # 执行多次直到报废
    actions = 0
    while device.perform_action():
        actions += 1

    assert not device.is_alive
    assert device.wear_and_tear >= 100.0
    assert device.health_ratio == 0.0
    assert actions > 0
    print(f"  ✅ 设备在 {actions} 次动作后报废")


def test_device_precision():
    """高精度设备磨损更快"""
    low = PhysicalDevice("低精度", precision=1.0)
    high = PhysicalDevice("高精度", precision=3.0)

    for _ in range(5):
        low.perform_action()
        high.perform_action()

    assert high.wear_and_tear > low.wear_and_tear
    print(f"  ✅ 高精度磨损 {high.wear_and_tear:.1f}% > 低精度 {low.wear_and_tear:.1f}%")


def test_network_burn():
    """代币销毁测试"""
    net = OpenCoinNetwork()
    assert net.total_supply == 100_000.0
    assert net.total_burned == 0.0

    tx = net.process_transaction(100.0, cycle=1, agent_name="test", device_name="test")
    assert tx.burned == 10.0
    assert net.total_supply == 99_990.0
    assert net.total_burned == 10.0
    assert len(net.ledger) == 1
    print(f"  ✅ 销毁 10.0，剩余供应量 {net.total_supply}")


def test_agent_payment():
    """Agent 支付测试"""
    agent = AIAgent("TestAI", coins=100.0)
    device = PhysicalDevice("TestDevice", precision=1.0)
    net = OpenCoinNetwork()

    assert agent.can_afford(device)

    result = agent.request_action(device, net, cycle=1)
    assert result is not None
    assert agent.coins < 100.0
    assert agent.cognitive_level > 1.0
    assert agent.actions_completed == 1
    print(f"  ✅ 支付 {result['cost']:.1f}，认知提升至 {result['cognitive_level']:.2f}")


def test_agent_insufficient_balance():
    """Agent 余额不足测试"""
    agent = AIAgent("PoorAI", coins=1.0)
    device = PhysicalDevice("ExpensiveDevice", precision=10.0)
    net = OpenCoinNetwork()

    assert not agent.can_afford(device)
    result = agent.request_action(device, net, cycle=1)
    assert result is None
    assert agent.actions_failed == 1
    print(f"  ✅ 余额不足正确拦截")


def test_simulator_single():
    """单Agent单设备完整模拟"""
    config = SimulationConfig(max_cycles=20)
    sim = Simulator(config)
    sim.add_agent("TestAI")
    sim.add_device("TestDevice", precision=2.0)

    result = sim.run(verbose=False)
    assert result.cycles > 0
    assert result.network_status["transactions"] > 0
    assert result.agents_status[0]["completed"] > 0
    print(f"  ✅ 模拟 {result.cycles} 轮，{result.network_status['transactions']} 笔交易")


def test_simulator_multi():
    """多Agent多设备竞争模拟"""
    config = SimulationConfig(max_cycles=30)
    sim = Simulator(config)
    sim.add_agent("Alpha")
    sim.add_agent("Beta")
    sim.add_device("Device-A", precision=2.0)
    sim.add_device("Device-B", precision=1.5)

    result = sim.run(verbose=False)
    assert result.cycles > 0
    # 两个 Agent 都应该有完成的动作
    total_completed = sum(a["completed"] for a in result.agents_status)
    assert total_completed > 0
    print(f"  ✅ 多Agent模拟 {result.cycles} 轮，共 {total_completed} 次动作")


if __name__ == "__main__":
    tests = [
        test_device_wear,
        test_device_precision,
        test_network_burn,
        test_agent_payment,
        test_agent_insufficient_balance,
        test_simulator_single,
        test_simulator_multi,
    ]

    print("\n🧪 OpenCoin 单元测试\n" + "-" * 40)
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 40}")
    print(f" 结果: {passed} 通过, {failed} 失败")
    print(f"{'=' * 40}\n")
    sys.exit(1 if failed > 0 else 0)
