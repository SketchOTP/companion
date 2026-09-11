# Mon construction model candidate — `MON_CONSTRUCTION_V1`

This is an authored, identity-locked construction model derived from the two
approved references. It is a candidate for operator review, not a replacement
for the canonical identity master.

## Grid and silhouette

- Work in a 1024×1024 square with the MON_FRAME_V1 root at `(512,896)`.
- The body is a rounded, unclothed purple form occupying approximately
  `x=260..764`, `y=420..920`; a seven-spike flame head stays inside the source
  safety rectangle `x=64..960,y=32..960`.
- The head silhouette is asymmetric by authored pose and direction; no runtime
  mirror is used as a distinct source.
- Ground contact is represented by two planted foot landmarks and a soft
  purple shadow footprint. Root translation is prohibited.

## Palette roles

| Role | Value | Use |
|---|---|---|
| outline | `#261444` | silhouette and limb separation |
| body | `#8b54d9` | primary purple fill |
| light | `#b879f2` | controlled cel highlight and pupils |
| shadow | `#5b3299` | controlled purple shadow shapes |
| eye | `#090711` | black eye fields |
| pupil | `#fff9ff` | white pupils |
| mouth | `#2b1238` | small simple mouth |

## Anatomy invariants

Every candidate must retain exactly two fingers plus one thumb on each hand and
exactly three toes on each foot. The head has edge spikes but no ears, horns,
muzzle, nose, teeth, clothes, accessories, symbols, or extra limbs. Face layers
may vary gaze, blink, and mouth presentation without changing identity.

## Pose limits

Squash/stretch is bounded to ±4% in source authoring; tilt is bounded to ±12°;
limb overlap may change but may not hide or invent digits; perspective offsets
remain within the turnaround's six-view proportions. Diagonal views are
explicitly candidate `front_left`, `front_right`, `back_left`, and `back_right`
views and are not operator-approved until visual review.

## Landmark set

`root`, `head`, `left_foot`, `right_foot`, `left_hand`, `right_hand`,
`gaze_center`, and `mouth_center` are recorded per drawing. Contacts are spans
over integer 1/24-second ticks; all authored source definitions carry a source
revision and checksum through the pack manifest.
