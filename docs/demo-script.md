# PlantOps demo script, for recording in Mattermost through Switch
Record in the real private room, plantops-sample-building-1, with sample data only. Keep the recording short, one site, one work order, one approval, one logged outcome.

## Before recording
- Docker Desktop running, Switch Console running, Claude Code signed in, agent is a member of the room.
- Room rules posted, sample register, weather, irrigation, and care log loaded as sample tools.
- Sample data only. No real building data.

## Scene 1, the problem, about 20 seconds
Manager, on camera or in chat, says in plain language: "We have a flagged plant in the lobby, and I need a plan before I change anything."
Show the room, the agent member, and the sample plant list if it is on screen.

## Scene 2, tag and triage, about 40 seconds
Manager posts in the room, tagging the exact agent name shown in the member list:
"@PlantOps Agent, check Sample Building 1 and propose the top work order for today."
Agent replies, citing all four inputs:
- Register: S-02, Lobby planter B, dry soil, drooping leaves, overdue since Oct 27, 2026.
- Weather: hot and dry for the next 2 days, do not wait for Day 3 rain.
- Irrigation: Zone B low flow on Oct 26, 2026, check before any schedule change.
- Care log: S-02 watered Oct 20, 2026, dry again Nov 2, 2026, no action yet.
Agent proposes WO-SAMPLE-001: Check Zone B low flow, water S-02 manually, recheck soil in 24 hours. Agent says clearly: no schedule change, no vendor dispatch, no payment, without approval.
Agent ends with: "Approve this work order? Reply Approve or Decline in this room."

## Scene 3, approval in chat, about 20 seconds
Manager replies in the room: "Approve"
Show the work order status change to Manager approved in the room, and say on camera: "That approval is in room history, the whole team can see who approved it and when."

## Scene 4, work done and logged outcome, about 30 seconds
Manager posts: "Work done, S-02 watered, Zone B checked, soil moist at recheck."
Agent replies: "Logged. WO-SAMPLE-001, Manager verified, Closed. Outcome: S-02 watered, Zone B low flow checked, recheck in 24 hours, next care Nov 10, 2026 for S-02 in the sample log."
Show the logged outcome in the room history.

## Scene 5, what breaks without Switch, about 20 seconds
On camera, in plain language: "Without Switch, there is no shared room, no shared history, and no approval trail in chat. The manager, the agent, and the vendor would be in separate chats, and no one could prove who approved what."
Do not claim Switch does payments, vendor calls, or accounting. It does not.

## Scene 6, scale and two-sided talk track, about 20 seconds, optional, no extra build
On camera: "Same room template, one room per building, for a property manager with many buildings. Same template, nursery, then client, then building, then planter, for a nursery that services client plants. That is the two-sided model, property managers on one side, nurseries on the other."
Do not build those extra rooms for this recording unless Jhonson gives a separate go.

## Recording notes
- Record the real room, not a slide deck pretending to be a room.
- Keep sample data on screen long enough to read, S-02, Zone B, WO-SAMPLE-001.
- End with the room history visible, showing tag, proposal, Approve, work done, and logged outcome, in that order.
