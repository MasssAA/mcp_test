# mcp-real-demo

一个真正可接入的 `stdio` MCP 服务示例，包含：

- 服务端 [mcp_server.py](D:\opencalw\teaching\mcp-real-demo\mcp_server.py)
- 探测客户端 [probe_client.py](D:\opencalw\teaching\mcp-real-demo\probe_client.py)
- 冒烟测试 [smoke_test.py](D:\opencalw\teaching\mcp-real-demo\smoke_test.py)
- 启动脚本 [start_mcp_server.bat](D:\opencalw\teaching\mcp-real-demo\start_mcp_server.bat)

这个目录中的代码使用标准 `Content-Length + JSON-RPC 2.0` 报文，可被支持 `stdio` 的 MCP Host 接入。

## 环境

- Python 3.10+

## 本地验证

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python .\probe_client.py
```

## 测试

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python .\smoke_test.py
```

成功时输出：

```text
REAL MCP SMOKE TEST PASSED
```

## 直接启动服务端

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python -X utf8 .\mcp_server.py
```

也可以直接运行：

```powershell
D:\opencalw\teaching\mcp-real-demo\start_mcp_server.bat
```

## Cherry Studio 配置

推荐使用 `STDIO` 方式：

- `Command`: `C:\Windows\System32\cmd.exe`
- `Arguments`: `/c D:\opencalw\teaching\mcp-real-demo\start_mcp_server.bat`

## 当前能力

### Tools

- `generate_test_case`
- `bug_triage`

### Resources

- `qa://checklists/web-regression`
- `qa://cases/login-success`

### Prompts

- `qa_daily_report`
