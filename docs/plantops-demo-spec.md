# PlantOps Agent, Flip the Switch demo spec
Status: build spec for Jhonson and Claude Code, Nov 2 evening. Nothing here is submitted. No production deploy, no repo push, no submission without Jhonson's separate go for each of those actions.

## Locked scope, do not expand
One sample site, one work order, one approval, one logged outcome, in a private Mattermost room through Switch.
- Manager tags PlantOps Agent in chat.
- Agent checks plant register, weather, irrigation status, and past care log, all sample data.
- Agent proposes one prioritized work order.
- Manager approves or declines in chat. No irrigation change happens without approval.
- Agent logs the outcome, so the next plan can use it.

## Room setup
- Room name, sample only: plantops-sample-building-1
- Room visibility: Private. Only invited members: property manager, PlantOps Agent, and, for the vendor scene only, the assigned sample vendor.
- Room rules, posted in the room:
  1. Sample data only. No real building, plant, or person names.
  2. The agent proposes, the manager decides. No irrigation change without a manager approval message in this room.
  3. Every decision stays in room history. Do not move approvals to a private message.
  4. One work order at a time for this demo. Do not open a second work order until the first is logged as closed.

## Tools, sample and mock only
These are tool definitions for the demo, not live connections to a real building.
1. plant_register: returns the sample site plant list, with location, plant type, condition, last care, next care.
2. weather: returns sample weather for the sample site, with heat, wind, and rain notes for the next 3 days.
3. irrigation_status: returns sample irrigation zones, with last run, next run, and any fault flag.
4. past_care_log: returns sample past care entries for the site, with date, action, and outcome.
5. work_order_log: appends a work order record, with status, approver, and outcome. Status list: Draft, Manager approved, Vendor notified, Vendor accepted, Vendor on site, Work done, Manager verified, Closed. For the core demo, only Draft, Manager approved, Work done, Manager verified, Closed are required. Vendor steps are the second scene, not the core.

## Triage logic, plain language
Agent reads, in order:
1. Condition flags in the register, worst first.
2. Weather risk for the next 3 days, heat or dry wind raises priority.
3. Irrigation faults, a fault on a zone with a flagged plant raises priority.
4. Overdue care, longest overdue first.
Agent proposes only the top item, with the reason in one sentence per input: register, weather, irrigation, care log. Agent must say what it will NOT do without approval, for example: no irrigation schedule change, no vendor dispatch, no payment.

## Approval gate, exact
- Agent message must end with: "Approve this work order? Reply Approve or Decline in this room."
- Manager reply must be the word Approve or Decline, in this room, to count.
- If Approve: agent updates the work order to Manager approved, then records work done only after the manager confirms work done in the room, then updates to Manager verified, then Closed, then logs the outcome.
- If Decline: agent updates the work order to Declined, logs the reason if the manager gives one, and stops. No work, no irrigation change.
- If the manager replies anything else: agent asks again for Approve or Decline, and does not proceed.

## What Switch does, for the README and video
- Switch connects Claude Code to the Mattermost room, so the agent appears as a teammate.
- The room keeps history, rules, tasks, and decisions, so the approval is visible to the whole team, not hidden in a private chat.
- Without Switch, there is no shared room, no shared history, and no approval trail in chat. Show that in the video by pointing to the room history, not by claiming a feature Switch does not have.
- Switch does not call vendors, pay vendors, or do accounting. A demo purchase order is a work order record only.

## Scale and two-sided notes, for the demo talk track only, not built tonight
- Property manager scale: one room per building, portfolio summary above them, team members only in their own building room unless they need portfolio access.
- Nursery scale: nursery workspace, then client, then building, then planter. Nursery manager sees all clients, crew sees only assigned buildings, client manager sees only their own buildings.
- These are talk track slides for the video, not extra rooms to build tonight, unless Jhonson gives a separate go for two more sample buildings and a nursery client room.

## Acceptance checks, before recording
1. Room is private, agent is a member, manager can tag the agent.
2. Tag triggers a proposal that cites register, weather, irrigation, and care log.
3. Proposal ends with the Approve or Decline prompt.
4. Approve in chat moves the work order to Manager approved, and no irrigation change is claimed before that approval.
5. Manager verified in chat moves the work order to Closed, and the outcome is logged and readable in the room.
6. Sample data only. No real building data.
