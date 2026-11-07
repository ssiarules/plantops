# PlantOps Agent

An agentic plant operations assistant in a team chat, for the Flip the Switch hackathon, Track 01 Best Business Workflow.

PlantOps Agent is built for two sides. On one side, organizations with plants across buildings and spaces, who need to track, nourish, and service them. On the other side, nurseries, plant sellers, and service providers, who upsell PlantOps and use it to track and service client plants better.

This repo is the demo project. It is not a live building deployment, and it uses sample data only.

## The demo loop, in order

1. Manager tags PlantOps Agent in a team chat room.
2. Agent checks the plant register, weather, irrigation status, and past care log.
3. Agent proposes one prioritized work order.
4. Manager approves or declines in chat. No irrigation change happens without approval.
5. Agent logs the outcome, so the next plan can use it.

Demo work order: WO-SAMPLE-001, Sample Building 1, plant S-02, Lobby planter B, dry soil, drooping leaves, overdue, Zone B low flow. Proposed action: check Zone B low flow, water S-02 manually, recheck soil in 24 hours.

## How Switch is used, central, not optional

Switch connects an existing agent, Claude Code in this demo, to a team chat room. The agent appears as a teammate, and the room keeps history, rules, tasks, and decisions.

In this demo, that room is a private Mattermost room, built into Switch, so no company Slack workspace is needed. The tag, the proposal, the approval, and the logged outcome all happen inside that room, in room history, visible to the whole team.

Without Switch, there is no shared room, no shared history, and no approval trail in chat. The manager, the agent, and the vendor would be in separate chats, and no one could prove who approved what.

Switch does not call vendors, pay vendors, or do accounting. A demo purchase order is a work order record only, not a real payment.

## Run the demo, without Switch, to check the logic

This repo includes a mock version of the same logic, so a judge or a teammate can run it without a Switch server.

```bash
python3 -m plantops.demo
```

That prints the tag, the proposal with one reason per input, the approval prompt, and, after approval in the script, the logged outcome. It does not change any real irrigation, and it does not call any real service.

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Run the demo, in Switch, for the recorded video

1. Docker Desktop running.
2. Switch Console installed, local server started.
3. Claude Code signed in via subscription, agent is a member of the private room.
4. Room name, sample only: plantops-sample-building-1, Private.
5. Room rules and agent instructions, from docs/switch-room-setup.md, posted in the room and set on the agent.
6. Sample data, from docs/sample-data.md, served to the agent by `python3 -m plantops.room`.
7. Manager tags the agent in the room, agent proposes WO-SAMPLE-001, manager replies Approve in the room, manager confirms work done, agent logs the outcome as Closed.
8. Record the real room, not slides pretending to be a room. Show tag, proposal, Approve, work done, and logged outcome, in that order.

Demo script for recording: docs/demo-script.md.

Demo video (unlisted): https://www.youtube.com/watch?v=zwkZ91sGdps

## Approval gate, exact

- Agent message must end with: "Approve this work order? Reply Approve or Decline in this room."
- Manager reply must be the word Approve or Decline, in this room, to count.
- If Approve: work order moves to Manager approved, then to Work done after the manager confirms work done, then to Manager verified, then to Closed, then the outcome is logged.
- If Decline: work order moves to Declined, the agent logs the reason if the manager gives one, and stops. No work, no irrigation change.
- If the manager replies anything else: agent asks again for Approve or Decline, and does not proceed.

## Sample data only

Sample data only. No real building data. Pricing below is draft only, until validated.

Draft pricing, not final:
- Single building: $49 to $99 per month.
- Portfolio: $39 to $79 per site per month.
- Nursery or service provider: $149 to $299 per month base, plus per managed client site.

## Scale and two-sided model, talk track

- Property manager scale: one room per building, portfolio summary above them, team members only in their own building room unless they need portfolio access.
- Nursery scale: nursery workspace, then client, then building, then planter. Nursery manager sees all clients, crew sees only assigned buildings, client manager sees only their own buildings.

## Repo structure

- `plantops/` - sample tools, triage, work order, and approval gate, with a CLI demo. `worker.py` is the worker checklist, photo step, and suggestions, used after Approve.
- `tests/` - tests for triage, approval, and logging.
- `docs/` - demo spec, sample data, demo script, and README outline used to build this repo.


## Three backend structures, one AI layer

Locked Nov 2, 2026. Full diagram: docs/backend-structures-diagram.html. Sample data only.

Scenario A, property management company, many buildings: building owner to portfolio manager in a central office, to building manager per building, to in-house crew or outside vendor. Central office holds portfolio, budgets, contracts, and approvals. Work starts as a call, text, email, or tenant note, then becomes a work order, a vendor dispatch, and an invoice. Routine work under a set cap is often handled without owner interruption, larger work needs owner approval.

Scenario B, nursery as service provider: nursery owner and sales, to account manager who owns a client portfolio, to crew lead who runs the morning meeting and inspects completed work, to field crew shared across clients, to client buildings. Sales sells plants and a service plan. Inside the nursery, growing and inventory run in parallel, and service meets sales at replacement time.

Scenario C, owner managed, or owner hires help directly: building owner to in-house caretaker, or to a nursery service contract, or to a management company, which falls back to Scenario A. In commercial buildings, the lease decides the zone: landlord or manager usually covers base building and common areas, tenant covers its own premises. Owner approval is direct and fast, and also a single point of failure if the caretaker leaves and the history leaves with them.

PlantOps Agent in between, in Switch: one room per building, portfolio summary above the building rooms, nursery workspace above its client buildings, permissions by room. Signal, photo, dry soil, schedule, weather, or irrigation, then agent triage from register, weather, irrigation, and care log, then proposed work order, then manager Approve or Decline in chat, then worker checklist for that plant and zone, then photo plus condition note, then suggestions with how to and tool needed, then work done with photo proof, then manager verifies, then logged outcome, closed. Then Phase 5, draft only: email draft with work order document, memo, and outcome log attached, posted in the room for manager approval before any send.

Who benefits: owner gets portfolio health, not one building at a time. Manager gets one tap approval in chat, same format across buildings. Nursery manager gets all clients with urgent conditions first, and replacements justified by condition and photo. Crew gets a checklist for that plant, not a vague task, and photo proof protects their work. Client manager gets proof in the room, not just an invoice at month end. No irrigation change, vendor dispatch, or payment happens before manager approval.

Demo mapping: core stays one sample building, one work order, one approval, one closed outcome, in a real Switch room. The other scenarios are talk track and this diagram in the README, not a live second demo, unless Jhonson gives a separate go for a second scene.

## Real world backend, and who does what

Demo today is sample only. Full diagram: docs/real-backend-architecture.html. Sample data only.

Where demo data comes from: local Python tools in this repo, plantops/data.py, triage.py, work_order.py, worker.py, reading a hardcoded sample register, S-01 to S-05, S-02 Lobby planter B, Zone B, sample weather, sample irrigation, sample care log, logged to a local state file. Switch does not provide plant, weather, or irrigation data. Switch is the chat transport. The agent provides data by running tools. In the demo, those tools read a sample file.

Where real data would come from, same flow, same approval gate, real adapters in place of data.py:
- Plant register: a database, Postgres or Supabase, tables for buildings, floors, zones, plants, planters, care logs, work orders.
- Weather: a weather API, by building address, cached hourly, not hardcoded.
- Irrigation: a vendor controller API, per building, per zone, read only first, zone status, flow, last run, faults. Control later, only after Manager Approve, via a gated tool, with an audit log.
- Care log and work orders: same database as the register, append only, never overwrite history.
- Photos and condition notes: room attachments, plus object storage linked from the work order id.
- People and permissions: room membership, plus a user table.

How the agent knows which building, which plant, which floor: room equals building. One Switch room per building, room metadata maps room_id to building_id, so a message from a building room already tells the agent the building, without asking the manager. A plant row then carries building, floor, room or office, planter, zone, type, condition, last care, next care. Triage joins register, weather, irrigation, and care log for that building, zone, and plant. If a source is missing, the agent says so plainly, it does not invent it.

Does the agent have tools outside Switch? Yes. Switch ships no agents and no models, and it does not replace the chat app. It connects an existing agent, through the Switch Agent Protocol, to a team chat room. That agent can use tools outside Switch, through MCP servers, HTTP APIs with keys held by the agent host, never posted in chat and never in the repo, database clients, and CLI tools in its working directory. Switch is one source of communication, not the only source of data. Chat is where people decide. Database, weather, irrigation, and photos are where data lives. The agent is the bridge, and the approval gate keeps that bridge safe.

Who does what, four roles, one room per building:
- Owner: portfolio view above building rooms, budget and larger work approval, portfolio health, not day to day plant checks. Sees summary across buildings, not every worker photo, unless they open a building room.
- Property manager: building room approval and verification. Receives the proposal, replies Approve or Decline in chat, verifies work done from photo and note, approves any email draft in the room before any send. No irrigation change, vendor dispatch, or payment happens before this approval.
- Nursery or service provider: client portfolio above client buildings. Nursery manager sees all clients, with urgent conditions first, and replacements justified by condition and photo, not just a sales note. Crew lead runs the morning meeting from the same work orders, inspects completed work from photo proof.
- Worker or crew, the most important role on site: physically at the plant, the only role that can take the real photo and do the real check. After Manager Approve, worker receives the S-02 checklist for that plant and zone only, in order: soil finger test, leaves, drainage, pot and roots, irrigation Zone B flow, photo. Worker uploads a clear photo of the plant and the soil surface, posts a condition note in the form Soil, leaves, drainage, irrigation, photo uploaded yes or no. Agent replies with suggested fix and maintenance, how to steps, and tool needed, with a short definition, no brands, no shopping links, suggestions only, not a certain diagnosis. If the photo could not be read, agent says so plainly and uses the condition note alone, never invents photo details. Worker then posts work done with photo proof, manager verifies from photo and note, agent logs the outcome and closes. Without the worker photo and note, there is no proof, no suggestion that matches the real plant, and no closed outcome that can be trusted.

Real build order, after the hackathon, one at a time: 1. Database register, with room to building mapping. 2. Weather API, read only. 3. Irrigation API, read only first. 4. Irrigation control, gated, only after Manager Approve, with audit log. 5. Photo storage linked to work order. Each step gets its own test and its own go. A real building deployment needs owner and manager approval, per building permissions, and sample data only in any public demo.

Plan for this hackathon: complete the basic Track 01 requirements first, core demo, clean video, README, submission package, then, if time before Nov 7, 2026 at 10:29 AM PT, submit the additional build out with it, Phase 4 worker view and this real world section, in the same submission, before the deadline, not after it.

## Hackathon

- Event: Flip the Switch, WeMakeDevs x DevTools Academy x Switch, Nov 4 to 7, 2026, online.
- Track: Best Business Workflow.
- Submissions close: Nov 7, 2026, 10:29 AM PT.
- Nothing in this repo is a submission by itself. Submission, via the WeMakeDevs event page, needs a separate go, with the exact repo, demo video, and README approved.
