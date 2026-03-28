# 真正可接入的 MCP Demo

这套示例和前一个“教学模拟版”不一样。

这里实现的是一个真正的 `stdio MCP server`：

- 使用 `Content-Length` 报文头
- 使用 `JSON-RPC 2.0`
- 支持标准初始化流程
- 支持 `tools`、`resources`、`prompts`

也就是说，这个服务不是“长得像 MCP”，而是“按 MCP 主机能识别的方式在通信”。

## 适合谁

- 想给测试同学做真实 MCP 上手体验的人
- 想把 demo 接进支持 MCP 的客户端里试用的人
- 想讲清楚 MCP 和普通函数调用区别的人

## 文件说明

- `mcp_server.py`: 真实 MCP 服务端
- `probe_client.py`: 本地探测客户端，用真正的 MCP 报文和服务端通信
- `smoke_test.py`: 自动验收脚本

## 运行方式

先进入目录:

```powershell
cd D:\opencalw\teaching\mcp-real-demo
```

### 1. 用本地探测客户端验证

```powershell
python .\probe_client.py
```

你会看到真实的 MCP 流程:

1. `initialize`
2. `notifications/initialized`
3. `ping`
4. `tools/list`
5. `tools/call`
6. `resources/list`
7. `resources/read`
8. `prompts/list`
9. `prompts/get`

### 2. 跑自动冒烟

```powershell
python .\smoke_test.py
```

成功时会输出:

```text
REAL MCP SMOKE TEST PASSED
```

## 如果要接入真正的 MCP Host

只要你的客户端支持 `stdio` 方式的 MCP server，本质上都是让宿主去启动下面这个命令:

```powershell
python -X utf8 D:\opencalw\teaching\mcp-real-demo\mcp_server.py
```

宿主启动后，就会通过标准输入输出和这个服务通信。

## 一个通用配置思路

不同 MCP 客户端的配置文件格式不一样，但核心信息通常都一样:

- `command`: `python`
- `args`: `["-X", "utf8", "D:\\opencalw\\teaching\\mcp-real-demo\\mcp_server.py"]`

如果某个客户端要求工作目录，也可以设置为:

- `cwd`: `D:\\opencalw\\teaching\\mcp-real-demo`

## 这个服务现在提供什么能力

### Tools

- `generate_test_case`: 根据功能描述生成测试用例草稿
- `bug_triage`: 根据缺陷严重度给出处理建议

### Resources

- `qa://checklists/web-regression`
- `qa://cases/login-success`

### Prompts

- `qa_daily_report`

## 课堂上怎么解释“它为什么是真的”

你可以直接这样说:

前一个 demo 是为了讲概念，通信方式是简化版。  
这个版本是真正按 MCP `stdio` 方式通信，报文是 `Content-Length + JSON-RPC`。  
所以它可以被真正的 MCP 宿主识别，而不只是我们自己写的普通脚本。

## 建议课堂动作

1. 先跑 `probe_client.py`
2. 再打开 [mcp_server.py](D:\opencalw\teaching\mcp-real-demo\mcp_server.py) 讲报文读写
3. 最后把它挂到你们实际使用的 MCP 客户端里

## 一句话总结

这套工程已经是“真 MCP 接入示例”，不是只用于讲概念的伪接口演示。
