# mcp-demo

一个本地可运行的 MCP 风格示例，包含：

- 服务端 [server.py](D:\opencalw\teaching\mcp-demo\server.py)
- 演示客户端 [client_demo.py](D:\opencalw\teaching\mcp-demo\client_demo.py)
- 冒烟测试 [smoke_test.py](D:\opencalw\teaching\mcp-demo\smoke_test.py)

这个目录中的代码使用简化通信方式，适合快速查看 `tools`、`resources`、`prompts` 的基本结构。

## 环境

- Python 3.10+

## 运行

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\client_demo.py
```

运行后会依次展示：

1. `initialize`
2. `tools/list`
3. `tools/call`
4. `resources/list`
5. `resources/read`
6. `prompts/list`
7. `prompts/get`

## 交互模式

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\client_demo.py --interactive
```

## 测试

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\smoke_test.py
```

成功时输出：

```text
SMOKE TEST PASSED
```

## 当前能力

### Tools

- `generate_test_case`
- `bug_triage`

### Resources

- `qa://checklists/web-regression`
- `qa://cases/login-success`

### Prompts

- `qa_daily_report`
