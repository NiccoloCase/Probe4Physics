# Research archive

The pre-release research state is preserved separately in
`../research-archive/pre-release-bbbb602/` beside the original repository.
It is a local archive, not a bundled download or a requirement for normal use.

The archive contains all 673 tracked regular files from commit
`bbbb6028c0fe984f3ceb9251c50c46443bec9c64`, an original-path SHA-256 manifest,
the repository/submodule state, the original local V-JEPA patch, and baseline
validation logs. Upstream submodule contents remain recoverable at their
recorded Git commits.

Historical runtime logs, generated notebook images, drafts, and planning notes
have been removed from the release checkout only after checksum verification.
[The removal inventory](archive-manifest.json) records their original paths,
sizes, and hashes. No result spreadsheets or CSV inputs were removed.

To recover an archived file, copy `files/<original-path>` from the archive to
the desired location, checking its SHA-256 against the manifest first. The
unchanged original main checkout and Git history also retain tracked content.
Do not restore historical documents over current release instructions.

Baseline test and notebook outcomes are summarized in [validation](validation.md).
