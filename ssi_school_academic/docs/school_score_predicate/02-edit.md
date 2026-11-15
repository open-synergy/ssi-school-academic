# Edit Score Predicate

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_predicate`\
> **Menu:** School > Configuration > Subject & Scoring > Score Predicates\
> **Actor:** user in group `Score Predicate`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Score Predicate already exists and has a Predicate Line.
- **Access:** User is in group `Score Predicate`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Score Predicates** menu.
2. Find and open the record to edit, then click **Edit**.
3. Change the **Name**.
4. On the **Predicate Lines** tab, click the **Minimum Score** cell of the line and
   enter the new score from 0 to 100.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- The new Minimum Score is used the next time a score is matched to a predicate.
