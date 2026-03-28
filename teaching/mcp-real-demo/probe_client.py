import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SERVER_PATH = ROOT / "mcp_server.py"


class MCPProbeClient:
    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            [sys.executable, "-X", "utf8", str(SERVER_PATH)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.next_id = 1

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            self.proc.wait(timeout=5)

    def _send(self, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        assert self.proc.stdin is not None
        self.proc.stdin.write(header)
        self.proc.stdin.write(body)
        self.proc.stdin.flush()

    def _read(self) -> dict[str, Any]:
        assert self.proc.stdout is not None
        headers: dict[str, str] = {}
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed the pipe unexpectedly.")
            if line == b"\r\n":
                break
            decoded = line.decode("ascii").strip()
            if ":" in decoded:
                name, value = decoded.split(":", 1)
                headers[name.lower()] = value.strip()
        content_length = int(headers["content-length"])
        body = self.proc.stdout.read(content_length)
        return json.loads(body.decode("utf-8"))

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": self.next_id,
            "method": method,
            "params": params or {},
        }
        self.next_id += 1
        self._send(payload)
        return self._read()

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        self._send(payload)


def pretty(title: str, data: dict[str, Any]) -> None:
    print(f"\n===== {title} =====")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> None:
    client = MCPProbeClient()
    try:
        pretty(
            "initialize",
            client.request(
                "initialize",
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "qa-probe", "version": "1.0.0"},
                },
            ),
        )
        client.notify("notifications/initialized")
        pretty("ping", client.request("ping"))
        pretty("tools/list", client.request("tools/list"))
        pretty(
            "tools/call",
            client.request(
                "tools/call",
                {
                    "name": "generate_test_case",
                    "arguments": {"feature_name": "订单支付", "risk_level": "high"},
                },
            ),
        )
        pretty("resources/list", client.request("resources/list"))
        pretty(
            "resources/read",
            client.request("resources/read", {"uri": "qa://cases/login-success"}),
        )
        pretty("prompts/list", client.request("prompts/list"))
        pretty("prompts/get", client.request("prompts/get", {"name": "qa_daily_report"}))
    finally:
        client.close()


if __name__ == "__main__":
    main()
