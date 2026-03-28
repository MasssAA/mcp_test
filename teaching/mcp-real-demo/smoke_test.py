from probe_client import MCPProbeClient


def main() -> None:
    client = MCPProbeClient()
    try:
        init = client.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "smoke-test", "version": "1.0.0"},
            },
        )
        assert init["result"]["serverInfo"]["name"] == "qa-mcp-real-demo"
        client.notify("notifications/initialized")

        tools = client.request("tools/list")
        names = [item["name"] for item in tools["result"]["tools"]]
        assert "generate_test_case" in names
        assert "bug_triage" in names

        case = client.request(
            "tools/call",
            {
                "name": "generate_test_case",
                "arguments": {"feature_name": "优惠券领取", "risk_level": "medium"},
            },
        )
        assert "优惠券领取" in case["result"]["content"][0]["text"]

        resource = client.request("resources/read", {"uri": "qa://checklists/web-regression"})
        assert "页面能正常打开" in resource["result"]["contents"][0]["text"]

        prompt = client.request("prompts/get", {"name": "qa_daily_report"})
        assert "测试日报" in prompt["result"]["messages"][0]["content"]["text"]

        print("REAL MCP SMOKE TEST PASSED")
    finally:
        client.close()


if __name__ == "__main__":
    main()
