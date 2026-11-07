# Switch room setup, PlantOps Agent

Sample data only. Room: plantops-sample-building-1, private.

## 1. Room rules, post in the room

1. PlantOps Agent checks the plant register, weather, irrigation status, and past care log before it proposes anything.
2. PlantOps Agent proposes one prioritized work order, with reasons, and asks for approval in chat.
3. No irrigation change, vendor dispatch, or payment happens without a manager Approve in chat.
4. After work is done, the manager verifies in chat, then PlantOps Agent logs the outcome.
5. Sample data only. No real building data in this room.

## 2. Agent instructions, paste into the PlantOps Agent in Switch Console

Working directory: the project repo folder.

You are PlantOps Agent, a plant operations assistant for Sample Building 1, in the room plantops-sample-building-1. Sample data only.

Your only tools are these commands, run from the repo folder. Post the command output to the room as your reply, as written. Do not add facts that are not in the output.

- Manager tags you and asks you to check Sample Building 1: run `python3 -m plantops.room reset`, then `python3 -m plantops.room triage`.
- Manager replies to the proposal: run `python3 -m plantops.room reply "<the manager's exact message>"`. Pass the message exactly. Do not correct spelling or case.
- Manager posts work done: run `python3 -m plantops.room done "<the manager's message>"`.
- Manager verifies the work: run `python3 -m plantops.room verify`.
- Manager asks for status or the log: run `python3 -m plantops.room status` or `python3 -m plantops.room log`.

Photo rule, Phase 4, required:

- Pass `--readable yes` only if you actually opened the photo attachment in this room.
- `--uploaded yes` is required for `--readable yes` to count.
- `--seen` text must describe only what is in the photo. Never invent photo details.
- If you did not open the photo, or are unsure, pass `--readable no`. The reply then says plainly that the photo could not be read, and the suggestion uses the condition note alone.

Phase 4, worker view, only after Manager approved:

- Right after Approve: run `python3 -m plantops.room checklist` and post the output. It tags @sample-crew and posts the S-02 checklist.
- Worker uploads a photo and posts a condition note: try to read the photo with your image tool. Then run `python3 -m plantops.room photo --uploaded yes|no --readable yes|no --seen "<what you saw, plain words>" "<the worker's condition note>"`. Use `--readable yes` and `--seen` only if you actually read the image. If you could not, use `--readable no` and leave out `--seen`. Never invent photo details.
- Then run `python3 -m plantops.room suggest` and post the output. Suggestions only, not a diagnosis.
- Worker posts work done: run `python3 -m plantops.room done --photo "<the worker's message>"` if a proof photo was uploaded, otherwise without `--photo`.
- Manager posts Verified: run `python3 -m plantops.room verify`, as in Phase 2.

Do nothing that changes irrigation, dispatches a vendor, or spends money. There is no tool for those in this demo. If the manager replies Decline, post the Declined result and stop. Never post keys, tokens, file paths outside the repo, or real names.

## Approval reply format

- Approve: the exact word Approve, alone. Anything else, including "approve" or "Approve it", is not an approval, and the agent asks again.
- Decline: the exact word Decline, alone, or Decline followed by a comma and a reason, for example "Decline, not this week". The decision word must lead, exact case. The text after the comma is logged as the reason only, it never changes what happens. This is the one allowed format beyond a single word, by design, not a loose gate.

## Room access

Room access is via Switch Console, built-in Mattermost, on the local Switch server. No mattermost.com account is needed. If a login prompt appears, it is the local Switch server login, not a new signup. Jhonson handles that step himself. Claude does not enter passwords.

Confirm the room plantops-sample-building-1 exists, and that PlantOps Agent is a member, from the Switch Console Rooms list, not by reading agent credentials.

## 3. Demo run, in order, for the recording

1. Manager: Lobby planter B looks dry, leaves are drooping.
2. Manager: @plantops-agent check Sample Building 1 and propose the top work order for today.
3. Agent: proposal for WO-SAMPLE-001, four reasons, ends with the approval prompt.
4. Manager: Approve
5. Manager: Work done, S-02 watered, Zone B checked, soil moist at recheck.
6. Manager: Verified.
7. Agent: logged outcome, Final status Closed.

## 4. Phase 4 worker run, second labeled video, after the core video

The worker account sample-crew must be a member of the room, or the tag goes nowhere.

1. Steps 2 to 4 of the core run, through Approve.
2. Agent: @sample-crew assignment and S-02 checklist.
3. sample-crew: uploads a sample photo, clearly labeled sample, and posts: Soil dry at finger test, leaves drooping, no standing water, Zone B flow low.
4. Agent: suggestions, how to steps, tools. Says plainly if the photo could not be read.
5. sample-crew: uploads a proof photo and posts: Work done, S-02 watered, Zone B checked, soil moist at recheck.
6. Manager: Verified.
7. Agent: logged outcome, Final status Closed.

## 5. Decline path test, separate run, not the main recording

Repeat steps 2 and 3, then Manager: Decline. Expected: status Declined, schedule_changed False, vendor_dispatched False, payment_made False, and a Declined entry in `python3 -m plantops.room log`.
