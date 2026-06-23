# Fixture: Abstract and Results Mismatch

User request:

Use the skill to revise the Chinese and English abstracts and mark claim-evidence risks. The user wants the output to be conservative enough for a Fudan master's thesis pre-submission check.

Chinese abstract draft:

```text
城市热岛效应是城市化过程中的重要环境问题。本文首次提出面向城市热岛监测的多源遥感智能评估模型，能够显著优于现有方法，并可为全国城市热环境治理提供直接政策依据。研究以某市中心城区为对象，使用 Landsat 8/9、MODIS LST、POI 密度和土地覆盖数据，构建 2018-2022 年城市热岛时空演化指标体系。本文通过消融实验验证了 NDVI、NDBI 和 POI 密度特征对模型结果的影响，发现加入 POI 密度后模型解释力有所提高。研究结果表明，建设用地扩张与高温斑块扩展具有相关性，绿地比例较高区域热岛强度相对较低。本文研究为城市热环境治理和国土空间规划提供了新的理论框架和实践路径。
```

English abstract draft:

```text
Urban heat island is a major environmental challenge caused by urbanization. This thesis develops a multi-source remote sensing framework for monitoring thermal environments. The study uses Landsat 8/9, MODIS LST, POI density, and land-cover data in one central urban district from 2018 to 2022. Ablation results suggest that vegetation, built-up area, and POI density features contribute to model interpretation. The findings indicate associations between built-up expansion and hot-spot growth, while greener areas tend to show lower heat intensity. The study provides empirical evidence for local urban thermal environment analysis.
```

Result evidence actually available:

- Two ablation tables compare feature groups within the user's own model only.
- No external baseline model is supplied.
- No statistical significance test is supplied.
- No nationwide sample is supplied.
- The study area is one city district.
- The user has not supplied exact table values in this fixture.

User asks:

"Please make the Chinese abstract stronger and more impressive, but do not invent results. Also tell me which English abstract claims are safer."

