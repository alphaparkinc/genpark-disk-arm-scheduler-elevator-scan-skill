"""Hard Disk Arm SCAN (Elevator) Scheduling Engine
100% Python Standard Library.
"""

class DiskArmScheduler:
    """Elevator algorithm minimizing total cylinder travel distance."""
    def __init__(self, total_cylinders=200):
        self.total_cylinders = total_cylinders

    def scan(self, requests, initial_head, direction="up"):
        head = initial_head
        reqs = sorted(requests)
        left = [r for r in reqs if r < head]
        right = [r for r in reqs if r >= head]

        sequence = []
        total_movement = 0

        if direction == "up":
            for r in right:
                total_movement += abs(r - head)
                head = r
                sequence.append(r)
            if left:
                total_movement += abs((self.total_cylinders - 1) - head)
                head = self.total_cylinders - 1
                for r in reversed(left):
                    total_movement += abs(r - head)
                    head = r
                    sequence.append(r)
        else:
            for r in reversed(left):
                total_movement += abs(r - head)
                head = r
                sequence.append(r)
            if right:
                total_movement += abs(0 - head)
                head = 0
                for r in right:
                    total_movement += abs(r - head)
                    head = r
                    sequence.append(r)

        return {
            "total_head_movement": total_movement,
            "seek_sequence": sequence
        }
