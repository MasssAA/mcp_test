# MCP Demo for Testers

这是一个给测试人员讲解 `MCP` 的完整教学 demo。

特点:

- 零依赖，只需要 `Python 3`
- 本地可运行，不需要联网
- 同时演示 `tools`、`resources`、`prompts`
- 附带自动验收脚本，方便课堂前自检

## 目录说明

- `server.py`: 一个最小可运行的 MCP Server
- `client_demo.py`: 演示客户端，既能脚本演示，也能交互操作
- `smoke_test.py`: 自动冒烟测试

## 这个 demo 能讲什么

适合给测试同学讲清楚这三件事:

1. `Tool` 是“让模型帮你做事”
2. `Resource` 是“让模型读资料”
3. `Prompt` 是“给模型一套现成提问模板”

把它翻成测试语言:

- `Tool` = 像“生成测试用例”“缺陷分级建议”这种动作
- `Resource` = 像“测试清单”“标准用例库”这种资料
- `Prompt` = 像“测试日报模板”这种固定问法

## 环境要求

- Python 3.10+

本机验证版本:

- Python 3.13.11

## 快速开始

在当前目录执行:

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\client_demo.py
```

你会看到一组已经编排好的调用流程，依次演示:

1. `initialize`
2. `tools/list`
3. `tools/call`
4. `resources/list`
5. `resources/read`
6. `prompts/list`
7. `prompts/get`

## 交互模式

如果你想在课堂上边讲边点:

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\client_demo.py --interactive
```

可做的操作包括:

- 查看工具列表
- 生成测试用例
- 获取缺陷分级建议
- 查看资源列表
- 读取登录测试用例
- 读取测试日报提示词

## 自动验收

上课前先跑一遍:

```powershell
cd D:\opencalw\teaching\mcp-demo
python .\smoke_test.py
```

如果成功，会输出:

```text
SMOKE TEST PASSED
```

## 课堂演示建议

### 第一段: 先讲白话

你可以直接这样说:

> MCP 就像给大模型接了一个标准插座。  
> 只要工具、资料、模板都按这个标准接进来，模型就知道怎么用。

### 第二段: 对照测试工作理解

- `tools/list`: 看这个系统都给了模型哪些能力
- `tools/call`: 真正调用某个能力
- `resources/list`: 看有哪些资料库
- `resources/read`: 读取具体资料
- `prompts/get`: 获取一套现成的提问模板

### 第三段: 带大家看代码

建议按这个顺序讲:

1. 看 [server.py](D:\opencalw\teaching\mcp-demo\server.py)
2. 再看 [client_demo.py](D:\opencalw\teaching\mcp-demo\client_demo.py)
3. 最后跑 [smoke_test.py](D:\opencalw\teaching\mcp-demo\smoke_test.py)

## 最适合课堂强调的点

### 1. Tool 不是聊天，是动作

例如:

- 生成测试用例
- 给缺陷分级建议

### 2. Resource 不是动作，是资料

例如:

- Web 回归清单
- 登录成功测试用例

### 3. Prompt 不是知识库，是模板

例如:

- 测试日报的固定提示词

## 你可以怎么改造成公司内部版本

把 `server.py` 里的示例能力，替换成你们自己的内容:

- 工具改成: 查询禅道缺陷、生成测试报告、读取接口状态
- 资源改成: 测试规范、项目用例库、回归 checklist
- 提示词改成: 日报模板、周报模板、上线检查模板

## 一句话总结

这个 demo 的价值，不是为了做一个复杂系统，而是为了让测试人员在 10 分钟内看懂:

`MCP = 用统一协议，把工具、资料、模板接给模型。`
