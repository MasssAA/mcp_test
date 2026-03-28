# MCP Demo Repository

这个仓库只保留两部分内容：

- 可运行代码
- 使用说明

包含两个示例：

- [teaching/mcp-demo](D:\opencalw\teaching\mcp-demo): 简化版示例
- [teaching/mcp-real-demo](D:\opencalw\teaching\mcp-real-demo): 真实 `stdio` MCP 示例

## 目录

```text
teaching/
  mcp-demo/
  mcp-real-demo/
```

## 快速开始

### 1. 简化版

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\client_demo.py
```

### 2. 真 MCP 版

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python .\probe_client.py
```

## 自检

### 简化版

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\smoke_test.py
```

### 真 MCP 版

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python .\smoke_test.py
```

## Cherry Studio 接入

真实 MCP 服务端文件在 [mcp_server.py](D:\opencalw\teaching\mcp-real-demo\mcp_server.py)。

推荐使用启动脚本 [start_mcp_server.bat](D:\opencalw\teaching\mcp-real-demo\start_mcp_server.bat)，在 Cherry Studio 的 `STDIO` 配置中填写：

- `Command`: `C:\Windows\System32\cmd.exe`
- `Arguments`: `/c D:\opencalw\teaching\mcp-real-demo\start_mcp_server.bat`

## 说明

- 没有保留 PPT、讲稿、教学备注
- 仓库现在只包含代码和运行说明
