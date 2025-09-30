# Manual QA - Bar Input Spacing

Date: 2025-07-03

## Scenario: Insert suggestion at start of textarea
- **Setup:** Empty textarea.
- **Action:** Trigger `insertAtCursor('word')`.
- **Result:** Textarea reads `word` with no leading space; cursor lands after `word`.

## Scenario: Insert suggestion in the middle of existing text
- **Setup:** Text `Keep going` with cursor between `Keep` and `going`.
- **Action:** Trigger `insertAtCursor('steady')`.
- **Result:** Textarea reads `Keep steady going` with exactly one space before `steady`; cursor lands after `steady`.

## Scenario: Insert suggestion at the end of the textarea
- **Setup:** Text `Stay sharp` with cursor at the end.
- **Action:** Trigger `insertAtCursor('focused')`.
- **Result:** Textarea reads `Stay sharp focused` with a single separating space; cursor lands after `focused`.
