# MCP Teaching Demos

这是一套给培训和课堂演示准备的 MCP 教学仓库，包含两个版本：

- [teaching/mcp-demo](D:\opencalw\teaching\mcp-demo): 教学模拟版，适合先讲清概念
- [teaching/mcp-real-demo](D:\opencalw\teaching\mcp-real-demo): 真实 `stdio` MCP 版，适合接入 Cherry Studio 等 MCP Host

## 仓库结构

```text
teaching/
  mcp-demo/
  mcp-real-demo/
```

## 两个版本的区别

### `mcp-demo`

用途：

- 给测试人员讲概念
- 先理解 `tools / resources / prompts`
- 不依赖真实 MCP Host

特点：

- 零依赖
- 自带脚本式演示客户端
- 适合 10-15 分钟课堂导入

### `mcp-real-demo`

用途：

- 给学员体验真实 MCP 接入
- 接入 Cherry Studio 等支持 MCP 的客户端
- 演示真正的 `stdio` 通信方式

特点：

- 使用 `Content-Length + JSON-RPC 2.0`
- 支持标准初始化流程
- 提供真实可接入的 `tools / resources / prompts`

## 快速开始

### 教学模拟版

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\client_demo.py
```

### 真 MCP 版

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python .\probe_client.py
```

## 自检

### 教学模拟版

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\smoke_test.py
```

### 真 MCP 版

```powershell
cd D:\opencalw\teaching\mcp-real-demo
python .\smoke_test.py
```

## 适合教学的使用顺序

1. 先讲 [teaching/mcp-demo](D:\opencalw\teaching\mcp-demo)，把概念讲明白
2. 再讲 [teaching/mcp-real-demo](D:\opencalw\teaching\mcp-real-demo)，让学员体验真实接入
3. 最后接到 Cherry Studio 做实际演示

## 当前状态

- 两套 demo 都已完成
- 两套 demo 都已本地验证通过
- 真 MCP 版已可用于 Cherry Studio 的 `STDIO` 模式接入
