# LLM-as-Judge Evaluation Framework (v3)

## Evaluation Dimensions

### 1. Factual Accuracy (事实准确性)

**Rubric**: Compare report claims against source data in staging directory.

**Prompt**:
```
你是报告质量评估专家。请对比以下报告与源数据，评估事实准确性。

报告文件: {report_path}
源数据目录: {staging_dir}
融合数据: {staging_dir}/fusion.md

评估标准:
- 报告中引用的 PR/Issue 编号是否在 fusion.md 中存在？
- 报告中描述的变更内容是否与源数据一致？
- 影响等级评估是否合理？

输出:
- accuracy_score: 1-5 (5=完全准确, 1=严重失实)
- inaccuracies: [列出具体不准确项]
```

### 2. Citation Accuracy (引用准确性)

**Rubric**: Verify all URLs and references point to valid sources.

**Prompt**:
```
请验证报告中所有超链接和引用的准确性。

报告文件: {report_path}
融合数据: {staging_dir}/fusion.md

评估标准:
- 所有 URL 是否在 fusion.md 数据中存在？（非编造）
- GitHub PR/Issue 链接格式是否正确？
- 每条动态是否包含源链接？

输出:
- citation_score: 1-5
- invalid_citations: [列出无效引用]
```

### 3. Completeness (完整性)

**Rubric**: Check all required sections and data items are present.

**Prompt**:
```
请评估报告的内容完整性。

报告文件: {report_path}
融合数据: {staging_dir}/fusion.md

评估标准:
- 是否包含全部 5 个必需章节？（概览、重点关注、社区动态、关键人物动态、附录）
- 社区动态列表是否包含 fusion.md 中所有通过筛选的条目？
- 概览是否覆盖了最重要的发现？
- 附录是否包含数据采集统计和数据源覆盖状态？

输出:
- completeness_score: 1-5
- missing_items: [列出缺失项]
```

### 4. Explainability (可解释性)

**Rubric**: Verify high-value items explain why they were selected.

**Prompt**:
```
请评估报告的可解释性。

报告文件: {report_path}

评估标准:
- 重点关注章节中每条 item 是否包含"入选原因"说明？
- 入选原因是否具体且有依据（非泛泛而谈）？
- 行动建议是否包含优先级和具体行动？

输出:
- explainability_score: 1-5
- missing_explanations: [列出缺少入选原因的 items]
```

### 5. Personalization (个性化匹配度)

**Rubric**: Check report content matches user role and focus areas.

**Prompt**:
```
请评估报告的个性化程度。

报告文件: {report_path}
用户角色文件: {user_prompt_path}

评估标准:
- 概览和重点关注是否侧重用户关注领域？
- 行动建议是否针对用户的具体角色？
- 内容详细程度是否匹配用户偏好？

输出:
- personalization_score: 1-5
- mismatches: [列出与用户角色不匹配的内容]
```

## Automated Evaluation Script

```bash
# Run evaluation on a specific report
REPORT="reports/pytorch_community_briefing_2026-03-26.md"
STAGING="reports/.staging/pytorch_2026-03-26_1d/"
USER_PROMPT="user-prompt.md"

# Evaluate each dimension
for dimension in factual citation completeness explainability personalization; do
    opencode run \
        --model alibaba-cn/qwen3.5-plus \
        -- "使用 tests/evaluate.md 中的 ${dimension} 维度评估 ${REPORT}，源数据在 ${STAGING}，用户角色在 ${USER_PROMPT}。输出 JSON 格式的评分结果。" \
        1>"tests/results/eval_${dimension}.json" \
        2>/dev/null
done
```

## Scoring Aggregation

| Dimension | Weight | Pass Threshold |
|-----------|--------|---------------|
| Factual Accuracy | 25% | >= 4 |
| Citation Accuracy | 20% | >= 4 |
| Completeness | 25% | >= 3 |
| Explainability | 15% | >= 3 |
| Personalization | 15% | >= 3 |

**Overall Pass**: Weighted average >= 3.5 AND no dimension below its threshold.

## v3 Agent Topology Validation

Beyond report quality, validate the v3 agent workflow:

```bash
# Check staging directory structure
STAGING="reports/.staging/pytorch_2026-03-26_1d/"
echo "=== Staging Structure ==="
ls -la "$STAGING"
# Expected files: github.md, community.md, fusion.md, analysis_*.md (0+)

# Check each staging file is non-empty
for f in github.md community.md fusion.md; do
    if [ -s "${STAGING}/${f}" ]; then
        echo "✅ ${f} exists and non-empty"
    else
        echo "❌ ${f} missing or empty"
    fi
done

# Check analysis files (optional)
ANALYSIS_COUNT=$(ls "${STAGING}"/analysis_*.md 2>/dev/null | wc -l)
echo "📊 Deep analysis files: ${ANALYSIS_COUNT}"
```
