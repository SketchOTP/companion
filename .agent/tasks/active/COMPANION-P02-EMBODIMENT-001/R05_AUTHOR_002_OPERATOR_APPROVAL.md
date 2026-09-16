# AUTHOR-002 operator visual selection — 2026-09-12

The operator said “Approved. These are much better” and, after Codex asked
whether this meant the construction sheet alone or the latest gait keys too,
clarified: “the construction sheet and the latest corrected gait poses”.

This is **operator visual approval**, not Codex self-approval. It supersedes
the prior coder non-acceptance for the selected artwork; it does not erase the
historical study observations or approve technical/runtime claims.

## Exact selection

R05_AUTHOR_002_OPERATOR_SELECTION.json binds eight construction facings and
eleven latest gait-key images to the existing source SHA-256 records. The sheet
is bound by SHA-256 77f149296c571a30d3d1c8d9f857f44e95f2e6b9d9af252d6c46c6552faa2ca1.
Construction cutout hashes are recorded separately from raw generation hashes.
“Latest” selects the final corrected version of each available study role:

- front — fc55cd4e25bad16e20d914f46864cf8d8d948a06b3a948a2fce3ff19bcb8acf3
- left_fix — a6d554e515a54bee013d5f31c8a085c5144bb822d1639192306b5660ccc28f5a
- right_fix — 6c33fd3606c08dd5d3a5827b1e53ec311497329f8f0278634c5f22ba40fc959f
- back — 649c100fb63b108ff8920578f3a4ade80a16254f88c6d55543a2630d3aa292b3
- front_left — 5efab37b753cccdf653514e5e9ecdbbc2804ab00186ec3649e5ba1d33c94740c
- front_right — b8a9c9d7b8fa119bee1247f82efb093301b48e4352b9b0301580809409380e04
- back_left — 4f03e9edfb52900dfd3bb1a22963c6656b6e982f94113446a472bbb28b00b259
- back_right — ded3a38b716e77c319d5710fc08fcbb6677d5015da19aa185ae0aed4dec14497
- left_contact_far — 340e99a4adc2f7ebbfaf1eba5f6498ecaeb70fff2d3d41ee29fed751d69c1128
- left_contact_near_armfix — b2e48b5bdbb9dd6a557019f2016b9a96198a49f14976420dc341724ea70a7ea1
- left_up_near — b8875de76ca33b6e0d7c2b179015b61ecbf7ee0de7cc3d913b0f5b069b6fd8a8
- left_passing_repair2 — fa8a0ef7696203afadadbd1bfd6718ca36a221f2694b75b64aa7845f9d577be4
- right_contact_near — 9c3c1464de5eca92743081e93989292729fb7b201321463575e63c435ae4b5a5
- left_passing_far — 872d4ccd262a1ea453000816bac86c339c5a432837efbf757413369562101c68
- left_down_armfix — 8e11373fd774d5d11738ae36b8b604e851a08f31ad74fac7fd47295977b81d08
- left_down_far — 6b8f0de7fa405ac7704b391389e59b3ebd9b453d27e82332f42bd959ff0fb036
- left_up_far — 4373d3b5836caa7c8da80ea85ff457bec07ac5c7850e4f48e2c534adb26c3d97
- right_contact_far — 42a39199c9d0fee003c43da798a6be900b0dc7388397b009b5e1ff17b716decd
- right_passing_near — 27cdfadfbaef13c03e5c194f23b721f23d08f5dcf2cff04e043c67d8525e6f05

Excluded superseded versions: left_initial, right_initial, left_contact_near, left_passing_near, left_down_near, left_passing_repair.
No raw or cutout image was edited, recompressed, replaced or deleted here.

## Remaining work

Keep the approved visual designs and poses as the reference selection for the
bounded v2 continuation. Complete left/right gait/action coverage, temporal
continuity, clean edges, MON_FRAME_V1 normalization, source/world contact QA and
actual v2 intake/Rust/Godot playback remain unfinished. The eleven gait keys are
not a complete pair of gait cycles. Approval does not invent missing frames.

No canonical source pack was promoted by this documentation-only change.
Future changed pixels/in-betweens are not automatically operator-approved.
R05-v1 and earlier superseded repair attempts remain rejected/historical.
Architecture v1.0 and accepted Phase01 are unchanged. Phase02 remains active
and unaccepted; Phase03+ remains closed. PR9 stays draft/open/unmerged; Issue8 open.

## Verification

Retrieval confidence ADEQUATE: current local/remote state and Notion/PR/Issue
were rechecked. Exact source hashes are independently rechecked before commit.
Documentation/selection recording only; no runtime or art-generation test was
claimed. Protected primary and unrelated secondary edits remain excluded.
