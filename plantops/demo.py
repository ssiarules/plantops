"""CLI demo of the locked chat loop, sample data only.

Run: python3 -m plantops.demo
This simulates the Mattermost room flow. It does not connect to Switch,
and it does not change any real irrigation, vendor, or payment.
"""

from .triage import proposal_message, propose_work_order
from .work_order import FINAL_OUTCOME, approve, log_outcome, mark_work_done, verify


def run_demo():
    """Run tag, proposal, Approve, work done, verified, Closed, logged."""
    print("Manager: @PlantOps Agent, check Sample Building 1 and propose the top work order for today.")
    order, reasons = propose_work_order()
    print()
    print(proposal_message(order, reasons))
    print()
    print("Manager: Approve")
    approved = approve(order, "Approve")
    print(f"Work order status: {order.status} (approved: {approved})")
    print("Manager: Work done, S-02 watered, Zone B checked, soil moist at recheck.")
    mark_work_done(order)
    verify(order)
    log_outcome(order, FINAL_OUTCOME)
    print(f"Logged outcome: {order.outcome}")
    print(f"Final status: {order.status}")
    return order


if __name__ == "__main__":
    run_demo()
