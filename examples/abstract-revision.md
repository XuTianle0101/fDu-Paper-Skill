# Example: Draft -> Claim-Evidence Audit

## Prompt

```text
Use $fdu-final-paper-skill to revise this Chinese abstract and check claim-evidence alignment.

原文：
本文研究了城市热岛问题，提出了一种新的分析方法。结果表明，该方法效果显著，
可以为城市治理提供重要参考。本文具有重要理论价值和实践意义。

已知证据：
- 数据：2013、2018、2023 年 Landsat 影像和 MODIS LST 数据。
- 方法：地表温度反演、Moran's I、GWR。
- 已验证结果：中心城区高温斑块向外围扩展；不透水面比例与 LST 呈正相关。
```

## Revised Abstract

城市热岛效应是高密度城市空间扩张过程中突出的生态环境问题。现有研究多关注单期地表温度分布，对多时期热岛格局演化及其空间异质性影响因素的综合解释仍有不足。本文以某城市中心城区为研究对象，基于 2013、2018 和 2023 年 Landsat 影像及 MODIS LST 数据，采用地表温度反演、空间自相关分析和地理加权回归方法，识别城市热岛的时空演化特征及主要影响因素。

研究发现，研究区高温斑块在 2013 至 2023 年间呈现由中心城区向外围扩展的趋势；不透水面比例与地表温度总体呈正相关关系，并在不同空间单元中表现出一定异质性。上述结果表明，多源遥感数据与空间统计模型相结合，能够为城市热环境识别和分区治理提供证据支持。本文的贡献在于构建了面向城市热岛演化分析的多源数据解释框架，并为后续热环境优化策略提供了空间分区依据。

## Claim-Evidence Risks

| Claim | Evidence status | Revision |
| --- | --- | --- |
| "提出一种新的分析方法" | Unsupported | Narrow to "构建多源数据解释框架" unless novelty is proven by literature review. |
| "效果显著" | Unsupported | Replace with specific verified results. |
| "重要理论价值" | Partially supported | Keep only if introduction and conclusion define theoretical contribution. |
| "治理参考" | Supported with limits | Tie to zoning or planning recommendations in a later chapter. |
