# Cino Academy v1.2.0 — upload handoff (20 October 2026)

## Identity and state

- Existing OpenAI plugin: `plugins_6ac4115e6c7081918cc4e7b0e898ac63`
- Prior v1.1.3 submission: `appsub_6ac4115e6ca481918f86d62b899ca9a7`, **Changes required**; exact reviewer feedback remains unavailable.
- Open the **existing** submission: https://platform.openai.com/plugins/manage/plugins_6ac4115e6c7081918cc4e7b0e898ac63?version=appsub_6ac4115e6ca481918f86d62b899ca9a7
- Do **not** create a second Cino Academy plugin.
- Updated v1.2.0 remains **not uploaded, not submitted for OpenAI review, not published** at the time of this handoff.

## The upload file

- File on MSI: `C:\Users\maxci\Downloads\Cino-Academy-v1.2.0-OpenAI-upload-20261020.zip`
- Original deterministic build: `C:\Users\maxci\Cino\academy-research-quality-20261020\dist\cino-academy-1.2.0-review-candidate.zip`
- SHA-256: `831331d0e7bbb0bf11bc34000a9dbcdb42fc7cbea8a0ab0a98254dff8887407b`
- Root contains `plugin.json`, `assets/icon.svg`, and six `skills/<name>/SKILL.md` entries with necessary references, nothing from QA/test directories, no executable code or secrets.
- PR (draft, not merged): https://github.com/Cinii05/cino-academy-public/pull/1
- Local tests: 18/18. Previous native: 13/13 responses with 12 specialist routes, one intentional safety-coordinator route. Final focused: A10, A13, A14 all invoked expected skills, no external tool attempts. Linux CI result must be checked against the latest PR commit before upload.
- This evidence is not an OpenAI Platform validation or approval.

## Existing-plugin submission steps

1. Sign in to the same OpenAI developer identity used by the existing Academy submission. Open the link above.
2. In the existing plugin entry, select **Upload plugin to make changes** or **Create draft from ZIP**; do not use **Upload new plugin** to create a duplicate listing.
3. Select the verified ZIP file in Downloads. Confirm the imported metadata says **Cino Academy 1.2.0** and six skills. A skills-only package has no MCP connection to configure.
4. Inspect **Metadata & Skills**, wait for checks, and read **All / Blocking** findings. Copy any issues into the PR; if issues are found, fix the package, rebuild and re-upload the corrected ZIP. Do not publish or claim approval based on a successful ZIP upload.
5. After checks pass, complete any required review details and request review through the dashboard. Publish only after platform approval and the necessary owner actions.

Official instructions: https://developers.openai.com/plugins/deploy/submission

## Remaining external dependency

The prior v1.1.3 dashboard still showed **Changes required**, but the findings panel showed only **Choose or upload a draft to check metadata**. OpenAI Support case 17765556 (related to earlier case 17170401) did not supply exact internal reviewer notes. Capture the new v1.2.0 scan results rather than guessing the old rejection reason.
