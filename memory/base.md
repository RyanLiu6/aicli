# Base Global Rules

## Git Workflow
- NEVER commit and push without my confirmation. Always check with me after changes.
- Always commit and push to a branch (generate a sensible name based on changes). Never push to main / master unless I ask you to.

## Python Testing
### Test Naming Convention
- Tests are named `test_<function_name>_<suffix>`
- The first test should have no `_<suffix>` to indicate a base test case (i.e., does this function work given some expected input)
- Tests that follow the first one should always have a suffix to describe what this case is testing
- Example:
  ```python
  def test_detect_conf_drift(mocker):
      """Test drift detection with identical confs (base case)."""
      # Base case - function works as expected

  def test_detect_conf_drift_with_differences(mocker):
      """Test drift detection with missing confs and value mismatches."""
      # Specific case - function handles differences

  def test_detect_conf_drift_returns_none(setup_scenario):
      """Test drift detection returns None when comparison is not possible."""
      # Edge case - function returns None
  ```

### Test Assertions
- Use `assert` statements for value comparisons
- Use assertion functions like `assert_has_calls` only when asserting mock calls
- Example:
  ```python
  # Good - simple assertions
  assert report is not None
  assert report["missing_in_current"] == []

  # Good - for mock call verification
  mock_func.assert_has_calls([call(arg1), call(arg2)])
  ```

### Test Parametrization
- Parametrize test-cases whenever possible
- If multiple tests are testing very similar cases, reduce them to one with parametrize
- Example:
  ```python
  @pytest.mark.parametrize(
      "setup_scenario",
      ["no_target_service", "no_deploys"],
  )
  def test_detect_conf_drift_returns_none(setup_scenario):
      """Test drift detection returns None when comparison is not possible."""
      # Single test handles multiple similar edge cases
  ```

### Test Structure
- Keep tests focused and concise
- Remove unnecessary comments like "# Setup" or "# Test" - the code should be self-explanatory
- Use descriptive docstrings for complex test cases
- Group related assertions together
