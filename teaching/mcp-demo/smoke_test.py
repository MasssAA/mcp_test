from client_demo import MCPDemoClient


def main() -> None:
    client = MCPDemoClient()
    try:
        init = client.request("initialize")
        assert init["result"]["serverInfo"]["name"] == "qa-mcp-demo"
        client.notify_initialized()

        tools = client.request("tools/list")
        tool_names = [item["name"] for item in tools["result"]["tools"]]
        assert "generate_test_case" in tool_names
        assert "bug_triage" in tool_names

        case = client.request(
            "tools/call",
            {
                "name": "generate_test_case",
                "arguments": {"feature_name": "订单提交", "risk_level": "high"},
            },
        )
        case_text = case["result"]["content"][0]["text"]
        assert "订单提交" in case_text

        resource = client.request("resources/read", {"uri": "qa://cases/login-success"})
        resource_text = resource["result"]["contents"][0]["text"]
        assert "LOGIN-001" in resource_text

        prompt = client.request("prompts/get", {"name": "qa_daily_report"})
        prompt_text = prompt["result"]["messages"][0]["content"]["text"]
        assert "测试日报" in prompt_text

        print("SMOKE TEST PASSED")
    finally:
        client.close()


if __name__ == "__main__":
    main()
