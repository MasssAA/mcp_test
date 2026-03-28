import datetime as dt
import os
import zipfile
from xml.sax.saxutils import escape


OUT = r"D:\opencalw\teaching\从MCP到Skill到Agent全流程_60min.pptx"


SLIDES = [
    ("从 MCP 到 Skill 到 Agent 全流程落地", ["60 分钟课程", "覆盖：MCP、Skill、模型加载、提示词、测试全流程 Agent"]),
    ("学习目标", ["理解 MCP 在架构中的位置", "掌握 Skill 设计与复用", "会做模型路由与提示词模板", "可落地测试全流程 Agent"]),
    ("全局架构", ["用户请求 -> Orchestrator", "MCP 统一接入 Tools/Resources", "Skill 固化执行方法", "Model Router 选择模型", "输出可执行结论"]),
    ("为什么是 MCP", ["标准化工具接入", "降低系统耦合", "增强可观测与可回放"]),
    ("MCP 核心对象", ["Tool：执行动作", "Resource：读取上下文", "Prompt/Template：复用提示片段", "Session Context：会话状态"]),
    ("Skill 的定义", ["Skill = 方法论 + 步骤 + 验收标准", "Skill 是能力模块，Agent 是总控系统", "先写 SKILL.md 再写脚本"]),
    ("Skill 最小结构", ["SKILL.md", "scripts/", "references/（可选）", "清晰输入输出与边界"]),
    ("模型加载策略", ["按质量/速度/成本选择", "轻任务走小模型", "复杂分析走大模型", "失败自动升级"]),
    ("模型路由流程", ["任务分类", "进入对应工作流", "失败重试升级", "统一格式输出"]),
    ("提示词三层结构", ["系统层：角色与边界", "任务层：目标与输入", "执行层：步骤与输出格式"]),
    ("提示词模板关键项", ["目标明确", "步骤可执行", "输出结构固定", "异常分支可处理"]),
    ("常见失败与修正", ["输出漂移 -> 固定模板", "过度执行 -> 增加约束", "幻觉命令 -> 工具白名单"]),
    ("落地案例目标", ["测试全流程 Skill Agent", "自动发现测试命令", "自动执行、归因、建议、回归"]),
    ("Skill 输入与输出", ["输入：repo_path / scope / auto_fix", "输出：摘要、失败清单、根因、修复计划、回归结果"]),
    ("课堂演示流程", ["打开失败测试仓库", "触发 test-e2e-skill", "观察调用链与结论", "修复并回归验证"]),
    ("示例提示词", ["角色：测试自动化代理", "步骤：发现命令->执行->归因->修复建议->回归", "约束：禁止破坏性操作与无关改动"]),
    ("质量门禁", ["可复现", "可解释", "可执行", "可回归"]),
    ("风险治理", ["白名单与沙箱执行", "数据脱敏与最小权限", "小步提交与可回滚"]),
    ("团队落地路径（4 周）", ["第 1 周：场景梳理", "第 2 周：封装 3 个 Skill", "第 3 周：接入路由与观测", "第 4 周：灰度上线"]),
    ("指标体系", ["效率：平均处理时长", "质量：一次通过率/回归通过率", "成本：任务成本", "稳定性：重试成功率"]),
    ("课堂练习", ["选一个测试痛点", "定义输入输出与验收标准", "设计路由规则与提示词"]),
    ("结论回顾", ["MCP 解决怎么连", "Skill 解决怎么做", "模型路由解决用谁做", "提示词解决产出形态"]),
    ("Q&A", ["建议先单场景做深", "先固定结构化输出", "先观测后自动修复"]),
    ("附录：test-e2e-skill 模板", ["Trigger / Input / Steps / Output / Constraints", "保证可追溯、可回滚、可验证"]),
]


def para(text, level=0):
    return (
        f"<a:p><a:pPr lvl=\"{level}\"/><a:r><a:rPr lang=\"zh-CN\" sz=\"2400\"/>"
        f"<a:t>{escape(text)}</a:t></a:r><a:endParaRPr lang=\"zh-CN\"/></a:p>"
    )


def text_box(spid, name, x, y, cx, cy, paragraphs, title=False):
    size = "4000" if title else "2200"
    body = "".join(
        f"<a:p><a:r><a:rPr lang=\"zh-CN\" sz=\"{size}\" b=\"{'1' if title else '0'}\"/>"
        f"<a:t>{escape(p)}</a:t></a:r><a:endParaRPr lang=\"zh-CN\"/></a:p>"
        for p in paragraphs
    )
    return f"""<p:sp>
<p:nvSpPr>
  <p:cNvPr id="{spid}" name="{escape(name)}"/>
  <p:cNvSpPr txBox="1"/>
  <p:nvPr/>
</p:nvSpPr>
<p:spPr>
  <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
  <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  <a:noFill/>
  <a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
  <a:bodyPr wrap="square"/>
  <a:lstStyle/>
  {body}
</p:txBody>
</p:sp>"""


def bullet_box(spid, bullets):
    paragraphs = []
    for i, b in enumerate(bullets):
        prefix = "• " + b
        paragraphs.append(
            f"<a:p><a:pPr marL=\"342900\" indent=\"-171450\" lvl=\"0\"/>"
            f"<a:r><a:rPr lang=\"zh-CN\" sz=\"2200\"/><a:t>{escape(prefix)}</a:t></a:r>"
            f"<a:endParaRPr lang=\"zh-CN\"/></a:p>"
        )
    body = "".join(paragraphs)
    return f"""<p:sp>
<p:nvSpPr>
  <p:cNvPr id="{spid}" name="Content"/>
  <p:cNvSpPr txBox="1"/>
  <p:nvPr/>
</p:nvSpPr>
<p:spPr>
  <a:xfrm><a:off x="685800" y="1828800"/><a:ext cx="11430000" cy="4114800"/></a:xfrm>
  <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  <a:noFill/>
  <a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
  <a:bodyPr wrap="square"/>
  <a:lstStyle/>
  {body}
</p:txBody>
</p:sp>"""


def slide_xml(title, bullets):
    title_shape = text_box(
        spid=2,
        name="Title",
        x=685800,
        y=457200,
        cx=11430000,
        cy=914400,
        paragraphs=[title],
        title=True,
    )
    content_shape = bullet_box(3, bullets)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {title_shape}
      {content_shape}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>
"""


def slide_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>
"""


def write_pptx(path):
    slide_count = len(SLIDES)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(
            "[Content_Types].xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
  <Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>
  <Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  {''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1, slide_count + 1))}
</Types>
""",
        )
        z.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
""",
        )
        z.writestr(
            "docProps/app.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office PowerPoint</Application>
  <Slides>24</Slides>
  <Notes>0</Notes>
  <HiddenSlides>0</HiddenSlides>
  <MMClips>0</MMClips>
  <ScaleCrop>false</ScaleCrop>
  <HeadingPairs>
    <vt:vector size="2" baseType="variant">
      <vt:variant><vt:lpstr>Theme</vt:lpstr></vt:variant>
      <vt:variant><vt:i4>1</vt:i4></vt:variant>
    </vt:vector>
  </HeadingPairs>
  <TitlesOfParts>
    <vt:vector size="1" baseType="lpstr"><vt:lpstr>Office Theme</vt:lpstr></vt:vector>
  </TitlesOfParts>
  <Company></Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0000</AppVersion>
</Properties>
""",
        )
        now = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        z.writestr(
            "docProps/core.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:dcmitype="http://purl.org/dc/dcmitype/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>从 MCP 到 Skill 到 Agent 全流程落地</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
""",
        )

        sld_ids = "".join(
            f'<p:sldId id="{256 + i}" r:id="rId{2 + i}"/>' for i in range(slide_count)
        )
        z.writestr(
            "ppt/presentation.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>{sld_ids}</p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle/>
</p:presentation>
""",
        )
        pres_rels = [
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        ]
        for i in range(1, slide_count + 1):
            pres_rels.append(
                f'<Relationship Id="rId{1+i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            )
        z.writestr(
            "ppt/_rels/presentation.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
"""
            + "\n".join(pres_rels)
            + """
</Relationships>
""",
        )
        z.writestr(
            "ppt/slideMasters/slideMaster1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles/>
</p:sldMaster>
""",
        )
        z.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>
""",
        )
        z.writestr(
            "ppt/slideLayouts/slideLayout1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>
""",
        )
        z.writestr(
            "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>
""",
        )
        z.writestr(
            "ppt/theme/theme1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme">
  <a:themeElements>
    <a:clrScheme name="Office">
      <a:dk1><a:srgbClr val="000000"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1F497D"/></a:dk2>
      <a:lt2><a:srgbClr val="EEECE1"/></a:lt2>
      <a:accent1><a:srgbClr val="4F81BD"/></a:accent1>
      <a:accent2><a:srgbClr val="C0504D"/></a:accent2>
      <a:accent3><a:srgbClr val="9BBB59"/></a:accent3>
      <a:accent4><a:srgbClr val="8064A2"/></a:accent4>
      <a:accent5><a:srgbClr val="4BACC6"/></a:accent5>
      <a:accent6><a:srgbClr val="F79646"/></a:accent6>
      <a:hlink><a:srgbClr val="0000FF"/></a:hlink>
      <a:folHlink><a:srgbClr val="800080"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Office">
      <a:majorFont><a:latin typeface="Calibri"/></a:majorFont>
      <a:minorFont><a:latin typeface="Calibri"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/>
  <a:extraClrSchemeLst/>
</a:theme>
""",
        )
        z.writestr(
            "ppt/presProps.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentationPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>
""",
        )
        z.writestr(
            "ppt/viewProps.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:viewPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
          xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:normalViewPr/>
  <p:slideViewPr/>
  <p:notesTextViewPr/>
  <p:gridSpacing cx="72008" cy="72008"/>
</p:viewPr>
""",
        )
        z.writestr(
            "ppt/tableStyles.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{00000000-0000-0000-0000-000000000000}"/>
""",
        )
        for i, (title, bullets) in enumerate(SLIDES, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(title, bullets))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels())


if __name__ == "__main__":
    write_pptx(OUT)
    print(OUT)
