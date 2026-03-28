import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SERVER_PATH = ROOT / "server.py"


class MCPDemoClient:
    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            [sys.executable, "-X", "utf8", str(SERVER_PATH)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        self._msg_id = 0

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            self.proc.wait(timeout=5)

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._msg_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._msg_id,
            "method": method,
            "params": params or {},
        }
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        return json.loads(line)

    def notify_initialized(self) -> None:
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()


def pretty_print(title: str, data: dict[str, Any]) -> None:
    print(f"\n===== {title} =====")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_scripted_demo() -> None:
    client = MCPDemoClient()
    try:
        pretty_print("1. initialize", client.request("initialize"))
        client.notify_initialized()
        pretty_print("2. tools/list", client.request("tools/list"))
        pretty_print(
            "3. tools/call -> generate_test_case",
            client.request(
                "tools/call",
                {
                    "name": "generate_test_case",
                    "arguments": {
                        "feature_name": "用户注册",
                        "risk_level": "high",
                    },
                },
            ),
        )
        pretty_print("4. resources/list", client.request("resources/list"))
        pretty_print(
            "5. resources/read",
            client.request("resources/read", {"uri": "qa://checklists/web-regression"}),
        )
        pretty_print("6. prompts/list", client.request("prompts/list"))
        pretty_print(
            "7. prompts/get",
            client.request("prompts/get", {"name": "qa_daily_report"}),
        )
    finally:
        client.close()


def run_interactive_demo() -> None:
    client = MCPDemoClient()
    try:
        pretty_print("initialize", client.request("initialize"))
        client.notify_initialized()

        menu = """
可选操作:
1. 查看工具列表
2. 生成测试用例
3. 缺陷分级建议
4. 查看资源列表
5. 读取登录测试用例
6. 读取测试日报提示词
0. 退出
"""
        while True:
            print(menu)
            choice = input("请输入编号: ").strip()
            if choice == "1":
                pretty_print("tools/list", client.request("tools/list"))
            elif choice == "2":
                feature_name = input("功能名称: ").strip() or "用户注册"
                risk_level = input("风险等级(low/medium/high): ").strip() or "medium"
                pretty_print(
                    "tools/call",
                    client.request(
                        "tools/call",
                        {
                            "name": "generate_test_case",
                            "arguments": {
                                "feature_name": feature_name,
                                "risk_level": risk_level,
                            },
                        },
                    ),
                )
            elif choice == "3":
                title = input("缺陷标题: ").strip() or "支付按钮点击无响应"
                severity = input("严重度(S1/S2/S3/S4): ").strip() or "S2"
                pretty_print(
                    "tools/call",
                    client.request(
                        "tools/call",
                        {
                            "name": "bug_triage",
                            "arguments": {"title": title, "severity": severity},
                        },
                    ),
                )
            elif choice == "4":
                pretty_print("resources/list", client.request("resources/list"))
            elif choice == "5":
                pretty_print(
                    "resources/read",
                    client.request("resources/read", {"uri": "qa://cases/login-success"}),
                )
            elif choice == "6":
                pretty_print(
                    "prompts/get",
                    client.request("prompts/get", {"name": "qa_daily_report"}),
                )
            elif choice == "0":
                break
            else:
                print("请输入 0-6 之间的编号。")
    finally:
        client.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_demo()
    else:
        run_scripted_demo()
