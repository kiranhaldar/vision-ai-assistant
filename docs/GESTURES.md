# Gesture Vocabulary

| Gesture                | Detection                          | Emitted Event         |
|------------------------|------------------------------------|-----------------------|
| Open Palm              | ≥4 fingers extended, state=idle    | `trigger: true`       |
| Pinch Start            | thumb–index dist < 0.045           | `gesture: pinch_start`|
| Pinch Active           | state=pinch, dist 0.02–0.15        | `scale: 0.4–2.0`      |
| Pinch End              | dist > 0.065                       | `gesture: pinch_end`  |
| Swipe Left/Right       | horizontal accumulation > 0.12     | `gesture: swipe_*`    |

## Tuning

Thresholds live in `.env`. Increase `PINCH_THRESHOLD` if pinches are
missed; decrease if false positives occur.