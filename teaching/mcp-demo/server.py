import json
import sys
from datetime import datetime
from typing import Any


PROTOCOL_VERSION = "2024-11-05"


QA_CHECKLIST = """# Web回归测试清单

1. 页面能正常打开
2. 登录成功后跳转正确
3. 关键按钮可点击
4. 表单校验提示正确
5. 提交后有成功反馈
"""


LOGIN_CASE = """# 登录测试用例

- 用例编号: LOGIN-001
- 标题: 正确账号密码登录
- 前置条件: 用户已注册
- 步骤:
  1. 打开登录页
  2. 输入正确账号和密码
  3. 点击登录
- 预期结果:
  1. 登录成功
  2. 跳转到首页
  3. 页面显示用户名
"""


def send_message(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def make_result(msg_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def make_error(msg_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": code, "message": message},
    }


def handle_initialize(msg_id: Any) -> dict[str, Any]:
    return make_result(
        msg_id,
        {
            "protocolVersion": PROTOCOL_VERSION,
            "serverInfo": {"name": "qa-mcp-demo", "version": "1.0.0"},
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {},
            },
        },
    )


def handle_tools_list(msg_id: Any) -> dict[str, Any]:
    return make_result(
        msg_id,
        {
            "tools": [
                {
                    "name": "generate_test_case",
                    "description": "根据功能描述生成测试用例草稿",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "feature_name": {"type": "string"},
                            "risk_level": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                        },
                        "required": ["feature_name"],
                    },
                },
                {
                    "name": "bug_triage",
                    "description": "根据缺陷严重度给出处理建议",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "severity": {
                                "type": "string",
                                "enum": ["S1", "S2", "S3", "S4"],
                            },
                        },
                        "required": ["title", "severity"],
                    },
                },
            ]
        },
    )


def handle_tools_call(msg_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    arguments = params.get("arguments", {})

    if name == "generate_test_case":
        feature_name = arguments.get("feature_name", "未命名功能")
        risk_level = arguments.get("risk_level", "medium")
        content = f"""测试用例草稿

功能名称: {feature_name}
风险等级: {risk_level}

建议覆盖点:
1. 正常流程
2. 异常输入
3. 权限边界
4. 重复提交
5. 接口超时/失败提示

示例步骤:
1. 进入 {feature_name} 页面
2. 输入合法数据
3. 提交操作
4. 校验页面反馈和后台状态
"""
        return make_result(msg_id, {"content": [{"type": "text", "text": content}]})

    if name == "bug_triage":
        title = arguments.get("title", "未命名缺陷")
        severity = arguments.get("severity", "S3")
        advice_map = {
            "S1": "立刻拉群处理，阻断发版，要求研发和测试同步跟踪。",
            "S2": "当天确认修复计划，优先回归主流程。",
            "S3": "排入当前迭代，回归相关功能即可。",
            "S4": "记录到缺陷池，按版本节奏统一处理。",
        }
        content = (
            f"缺陷标题: {title}\n"
            f"严重度: {severity}\n"
            f"处理建议: {advice_map.get(severity, '请人工评估优先级。')}"
        )
        return make_result(msg_id, {"content": [{"type": "text", "text": content}]})

    return make_error(msg_id, -32602, f"未知工具: {name}")


def handle_resources_list(msg_id: Any) -> dict[str, Any]:
    return make_result(
        msg_id,
        {
            "resources": [
                {
                    "uri": "qa://checklists/web-regression",
                    "name": "Web回归测试清单",
                    "description": "适合课堂演示的基础回归清单",
                    "mimeType": "text/markdown",
                },
                {
                    "uri": "qa://cases/login-success",
                    "name": "登录成功测试用例",
                    "description": "登录模块示例用例",
                    "mimeType": "text/markdown",
                },
            ]
        },
    )


def handle_resources_read(msg_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    uri = params.get("uri")
    content_map = {
        "qa://checklists/web-regression": QA_CHECKLIST,
        "qa://cases/login-success": LOGIN_CASE,
    }
    if uri not in content_map:
        return make_error(msg_id, -32602, f"未知资源: {uri}")
    return make_result(
        msg_id,
        {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/markdown",
                    "text": content_map[uri],
                }
            ]
        },
    )


def handle_prompts_list(msg_id: Any) -> dict[str, Any]:
    return make_result(
        msg_id,
        {
            "prompts": [
                {
                    "name": "qa_daily_report",
                    "description": "生成测试日报提示词模板",
                }
            ]
        },
    )


def handle_prompts_get(msg_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    if name != "qa_daily_report":
        return make_error(msg_id, -32602, f"未知提示词: {name}")
    today = datetime.now().strftime("%Y-%m-%d")
    return make_result(
        msg_id,
        {
            "description": "测试日报模板",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": (
                            f"请生成 {today} 的测试日报，包含：\n"
                            "1. 今日执行用例数\n"
                            "2. 新增缺陷数\n"
                            "3. 阻塞问题\n"
                            "4. 明日计划"
                        ),
                    },
                }
            ],
        },
    )


def dispatch(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    msg_id = message.get("id")
    params = message.get("params", {})

    if method == "initialize":
        return handle_initialize(msg_id)
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return handle_tools_list(msg_id)
    if method == "tools/call":
        return handle_tools_call(msg_id, params)
    if method == "resources/list":
        return handle_resources_list(msg_id)
    if method == "resources/read":
        return handle_resources_read(msg_id, params)
    if method == "prompts/list":
        return handle_prompts_list(msg_id)
    if method == "prompts/get":
        return handle_prompts_get(msg_id, params)
    return make_error(msg_id, -32601, f"未知方法: {method}")


def main() -> None:
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            send_message(make_error(None, -32700, "无效 JSON"))
            continue

        response = dispatch(message)
        if response is not None:
            send_message(response)


if __name__ == "__main__":
    main()
