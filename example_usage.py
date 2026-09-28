from client import DiskArmScheduler

def main():
    disk = DiskArmScheduler(total_cylinders=200)
    reqs = [98, 183, 37, 122, 14, 124, 65, 67]
    res = disk.scan(reqs, initial_head=53, direction="up")
    print("Disk Arm SCAN Scheduler Verification:")
    print(f"Total Movement: {res['total_head_movement']} cylinders")
    print(f"Service Order: {res['seek_sequence']}")

if __name__ == "__main__":
    main()
