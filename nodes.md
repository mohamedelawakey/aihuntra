```
START
  ↓
profile_loader_node ✅
  ↓
cv_parsing_node ✅
  ↓
job_search_node
  ↓
job_normalization_node
  ↓
job_filtering_node
  ↓
job_analysis_node
  ↓
match_scoring_node
  ↓
cv_tailoring_node
  ↓
cover_letter_node
  ↓
decision_node
  ↓
tracking_node
  ↓
human_approval_node
  ↓
END


IF match_score >= minimum_match_score
  → cv_tailoring_node
ELSE
  → tracking_node as SKIPPED

```
