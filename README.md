# ai-assistant-ui
User Interface for Support AI Assistant

## Branching Naming Conventions

We follow a trunk-based development approach to keep our workflow streamlined and efficient. Below are the guidelines for creating branches for various purposes:

### Main Branch
- **`main`**: The trunk branch where all changes are integrated. It should always be in a deployable state.

### Short-Lived Branches
All work is done on short-lived branches that are frequently merged back into `main`. These branches should be kept simple and focused, often representing a single task or bug fix.

### Feature Branches
Feature branches are used for developing new features. Since we follow a trunk-based approach, these branches should be short-lived, with frequent merges back into `main`.

- **Branch Name Format**: `feature/{short-description}`
- **Examples**:
  - `feature/user-authentication`
  - `feature/dashboard-ui`
  
- **Guidelines**:
  - Create a feature branch directly off `main`.
  - Frequently merge your feature branch back into `main` to minimize divergence.
  - Keep the branch life short—merge back as soon as the feature is ready.

### Bug Fix Branches
Bug fix branches are used for addressing specific issues or bugs. Like feature branches, these should also be short-lived.

- **Branch Name Format**: `bugfix/{issue-id}-{short-description}`
- **Examples**:
  - `bugfix/123-login-error`
  - `bugfix/456-api-timeout`
  
- **Guidelines**:
  - Create a bug fix branch directly off `main`.
  - Merge back into `main` as soon as the bug is fixed.

### Hotfix Branches
Hotfix branches are used for urgent fixes that need to be deployed immediately, usually to resolve issues in production.

- **Branch Name Format**: `hotfix/{short-description}`
- **Examples**:
  - `hotfix/critical-security-patch`
  - `hotfix/fix-crashing-bug`
  
- **Guidelines**:
  - Create a hotfix branch directly off `main`.
  - Merge back into `main` as soon as the fix is verified and ready for deployment.

### Experimental Branches (Optional)
If there’s a need to test out a new idea or experiment, create an experimental branch. These branches should still be short-lived and regularly synced with `main`.

- **Branch Name Format**: `experiment/{short-description}`
- **Examples**:
  - `experiment/new-algorithm`
  - `experiment/ui-concept`
  
- **Guidelines**:
  - Create an experimental branch off `main`.
  - Merge back into `main` if the experiment is successful.

### Workflow
1. Create a new branch off `main` for any new feature, bug fix, or hotfix.
2. Make your changes in the branch.
3. Push the branch to the remote repository.
4. Frequently merge changes from `main` into your branch to stay up-to-date.
5. Create a pull request (PR) to merge the branch back into `main`.
6. Once the PR is approved and merged, the branch can be deleted.

By adhering to this trunk-based branching strategy, we ensure continuous integration and a consistent, deployable codebase at all times.
