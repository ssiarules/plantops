# PlantOps demo, sample data only
Sample data only. No real building data. All names, plants, zones, and dates below are invented for the demo.

## Sample site
- Site name: Sample Building 1
- Site type: Office building, sample only
- Room: plantops-sample-building-1, Private
- Manager, sample role only: Sample Property Manager
- Vendor, sample role only, second scene only: Sample Vendor

## Plant register, Sample Building 1
| Plant ID | Location, sample | Plant type, sample | Condition | Last care | Next care |
| S-01 | Lobby planter A | Sample ficus | Good, leaves firm | Oct 28, 2026 | Nov 10, 2026 |
| S-02 | Lobby planter B | Sample ficus | Flagged, dry soil, drooping leaves | Oct 20, 2026 | Overdue, was Oct 27, 2026 |
| S-03 | Hallway planter | Sample snake plant | Good | Oct 30, 2026 | Nov 13, 2026 |
| S-04 | Meeting room planter | Sample pothos | Fair, light yellowing on 2 leaves | Oct 25, 2026 | Nov 6, 2026 |
| S-05 | Kitchen planter | Sample peace lily | Good | Oct 29, 2026 | Nov 12, 2026 |

Top triage item for the demo: S-02, dry soil, drooping leaves, overdue since Oct 27, 2026.

## Weather, sample, next 3 days
- Day 1: Hot and dry, high 88, no rain, dry wind.
- Day 2: Hot and dry, high 90, no rain.
- Day 3: Cooler, high 78, light rain possible.
Weather note for S-02: hot and dry wind raises priority, do not delay watering to Day 3.

## Irrigation status, sample
- Zone A, Lobby: Last run Oct 30, 2026. Next run Nov 3, 2026. Status: OK.
- Zone B, Lobby planters S-01 and S-02: Last run Oct 26, 2026. Next run Nov 3, 2026. Status: Flagged, low flow on last run, check before changing schedule.
- Zone C, Hallway and meeting rooms: Last run Oct 30, 2026. Next run Nov 4, 2026. Status: OK.
Irrigation note for the demo: agent proposes a check and a manual water for S-02, not a schedule change, until the manager approves. No schedule change happens without approval.

## Past care log, sample
- Oct 20, 2026: S-02 watered, soil dry at check, 1 gallon, outcome good for 3 days.
- Oct 26, 2026: Zone B irrigation run, low flow noted, no schedule change made.
- Oct 28, 2026: S-01 watered, outcome good.
- Oct 30, 2026: Zone A and Zone C runs, outcome OK.
- Nov 2, 2026: S-02 check, soil dry again, drooping leaves noted, no action taken yet, awaiting manager decision.

## Work order, demo, one only
- Work order ID: WO-SAMPLE-001
- Site: Sample Building 1
- Plant: S-02, Lobby planter B
- Proposed action: Check Zone B low flow, water S-02 manually, recheck soil in 24 hours.
- What it is not: not a schedule change, not a vendor payment, not a plant replacement.
- Cost cap, sample only: $0 in the core demo, no payment. Vendor scene, if shown, uses a sample cost cap only, draft pricing only, no real payment.
- Status flow: Draft, Manager approved, Work done, Manager verified, Closed.

## Nursery sample, talk track only, not built tonight
- Nursery, sample only: Sample Nursery Co.
- Client, sample only: Sample Client 1
- Client buildings, sample only: Sample Client Building A, Sample Client Building B
- Planter, sample only: Client Building A, Lobby planter, sample ficus, condition good, last care Oct 29, 2026.
Use this only to explain the two-sided model in the video talk track, unless Jhonson gives a separate go to build a nursery room.
