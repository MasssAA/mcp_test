import json
import sys
from datetime import datetime
from typing import Any


PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "qa-mcp-real-demo", "version": "1.0.0"}


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


def send_packet(message: dict[str, Any]) -> None:
    body = json.dumps(message, ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def read_packet() -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line == b"\r\n":
            break
        decoded = line.decode("ascii").strip()
        if ":" not in decoded:
            continue
        name, value = decoded.split(":", 1)
        headers[name.lower()] = value.strip()

    content_length = int(headers.get("content-length", "0"))
    if content_length <= 0:
        return None
    body = sys.stdin.buffer.read(content_length)
    return json.loads(body.decode("utf-8"))


def make_result(msg_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def make_error(msg_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": code, "message": message},
    }


def initialize_result(msg_id: Any) -> dict[str, Any]:
    return make_result(
        msg_id,
        {
            "protocolVersion": PROTOCOL_VERSION,
            "serverInfo": SERVER_INFO,
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False},
                "prompts": {"listChanged": False},
            },
        },
    )


def tools_list_result(msg_id: Any) -> dict[str, Any]:
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
                            "feature_name": {
                                "type": "string",
                                "description": "要测试的功能名称",
                            },
                            "risk_level": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "风险等级",
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
                            "title": {"type": "string", "description": "缺陷标题"},
                            "severity": {
                                "type": "string",
                                "enum": ["S1", "S2", "S3", "S4"],
                                "description": "缺陷严重度",
                            },
                        },
                        "required": ["title", "severity"],
                    },
                },
            ]
        },
    )


def tool_content(text: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": False}


def tools_call_result(msg_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    arguments = params.get("arguments", {})

    if name == "generate_test_case":
        feature_name = arguments.get("feature_name", "未命名功能")
        risk_level = arguments.get("risk_level", "medium")
        text = f"""测试用例草稿

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
        return make_result(msg_id, tool_content(text))

    if name == "bug_triage":
        title = arguments.get("title", "未命名缺陷")
        severity = arguments.get("severity", "S3")
        advice_map = {
            "S1": "立刻拉群处理，阻断发版，要求研发和测试同步跟踪。",
            "S2": "当天确认修复计划，优先回归主流程。",
            "S3": "排入当前迭代，回归相关功能即可。",
            "S4": "记录到缺陷池，按版本节奏统一处理。",
        }
        text = (
            f"缺陷标题: {title}\n"
            f"严重度: {severity}\n"
            f"处理建议: {advice_map.get(severity, '请人工评估优先级。')}"
        )
        return make_result(msg_id, tool_content(text))

    return make_error(msg_id, -32602, f"未知工具: {name}")


def resources_list_result(msg_id: Any) -> dict[str, Any]:
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


def resources_read_result(msg_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    uri = params.get("uri")
    content_map = {
        "qa://checklists/web-regression": QA_CHECKLIST,
        "qa://cases/login-success": LOGIN_CASE,
    }
    text = content_map.get(uri)
    if text is None:
        return make_error(msg_id, -32602, f"未知资源: {uri}")
    return make_result(
        msg_id,
        {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/markdown",
                    "text": text,
                }
            ]
        },
    )


def prompts_list_result(msg_id: Any) -> dict[str, Any]:
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


def prompts_get_result(msg_id: Any, params: dict[str, Any]) -> dict[str, Any]:
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
        return initialize_result(msg_id)
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return make_result(msg_id, {})
    if method == "tools/list":
        return tools_list_result(msg_id)
    if method == "tools/call":
        return tools_call_result(msg_id, params)
    if method == "resources/list":
        return resources_list_result(msg_id)
    if method == "resources/read":
        return resources_read_result(msg_id, params)
    if method == "prompts/list":
        return prompts_list_result(msg_id)
    if method == "prompts/get":
        return prompts_get_result(msg_id, params)
    return make_error(msg_id, -32601, f"未知方法: {method}")


def main() -> None:
    while True:
        message = read_packet()
        if message is None:
            break
        response = dispatch(message)
        if response is not None:
            send_packet(response)


if __name__ == "__main__":
    main()
