# Changelog

## [2.0.0](https://github.com/shipshitdev/skills/compare/v1.3.0...v2.0.0) (2026-08-30)


### ⚠ BREAKING CHANGES

* consolidate test/scan/env/prompt/performance commands behind skills ([#127](https://github.com/shipshitdev/skills/issues/127))
* rename release-cleanup to git-cleanup behind /cleanup, retire /clean and /inbox ([#125](https://github.com/shipshitdev/skills/issues/125))

### Features

* add gh-board-sync skill and expand /board into a full front door ([#126](https://github.com/shipshitdev/skills/issues/126)) ([7e30880](https://github.com/shipshitdev/skills/commit/7e30880753c9d9e2a8660e8ddaeac20b3ba9111f))
* consolidate test/scan/env/prompt/performance commands behind skills ([#127](https://github.com/shipshitdev/skills/issues/127)) ([9a403e2](https://github.com/shipshitdev/skills/commit/9a403e230cf0dfe9c8f3407fa7f9dde6049b6ca6))
* rename release-cleanup to git-cleanup behind /cleanup, retire /clean and /inbox ([#125](https://github.com/shipshitdev/skills/issues/125)) ([43d321a](https://github.com/shipshitdev/skills/commit/43d321a7f665583a785a0175d8aa3da46ec85351))

## [1.3.0](https://github.com/shipshitdev/skills/compare/v1.2.0...v1.3.0) (2026-08-28)


### ⚠ BREAKING CHANGES

* hard-rename deslop and monitor QA runtime errors ([#120](https://github.com/shipshitdev/skills/issues/120))

### Features

* hard-rename deslop and monitor QA runtime errors ([#120](https://github.com/shipshitdev/skills/issues/120)) ([1cac5d9](https://github.com/shipshitdev/skills/commit/1cac5d9455de92040fb869c4c63ffddb6f38098c))

## [1.2.0](https://github.com/shipshitdev/skills/compare/v1.1.1...v1.2.0) (2026-08-27)


### Features

* port Lauren Tan pstack skills and recut tdd/de-slop ([#119](https://github.com/shipshitdev/skills/issues/119)) ([e983aba](https://github.com/shipshitdev/skills/commit/e983abae69365fc68d346e311044e168c081eef7))


### Bug Fixes

* **skills:** write disposable scratch to the current repo .tmp ([#116](https://github.com/shipshitdev/skills/issues/116)) ([5d747b4](https://github.com/shipshitdev/skills/commit/5d747b4b10a6a82dc081ba95ed2fa09d29540575))

## [1.1.1](https://github.com/shipshitdev/skills/compare/v1.1.0...v1.1.1) (2026-08-18)


### Chores

* drop the no-op CI dispatch from the release workflow ([#113](https://github.com/shipshitdev/skills/issues/113)) ([9e6af98](https://github.com/shipshitdev/skills/commit/9e6af9852718d57ecb43ba580b2f3ed5d1e85b2a))
* open the release PR as a draft ([#115](https://github.com/shipshitdev/skills/issues/115)) ([ddeb8fe](https://github.com/shipshitdev/skills/commit/ddeb8fe66250b7b842c4935d08d8df74210c4581))

## [1.1.0](https://github.com/shipshitdev/skills/compare/v1.0.0...v1.1.0) (2026-08-17)


### Features

* add release-please for automated versioning and GitHub releases ([#110](https://github.com/shipshitdev/skills/issues/110)) ([90e47be](https://github.com/shipshitdev/skills/commit/90e47be70d76cc22e584b842d20b5635bc7e719b))


### Bug Fixes

* run release-please on GITHUB_TOKEN and dispatch CI on the release branch ([#111](https://github.com/shipshitdev/skills/issues/111)) ([4a063e6](https://github.com/shipshitdev/skills/commit/4a063e6ced1fdb5d7b9b790985c195d1f2f3dba7))
