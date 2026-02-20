def towers_of_hanoi(n, source, auxiliary, target):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    # Move n-1 disks from source to auxiliary peg
    towers_of_hanoi(n - 1, source, target, auxiliary)
    
    # Move the remaining disk from source to target
    print(f"Move disk {n} from {source} to {target}")
    
    # Move the n-1 disks from auxiliary to target peg
    towers_of_hanoi(n - 1, auxiliary, source, target)

# Main Program
num_disks = int(input("Enter the number of disks: "))
print(f"\nSteps to solve Tower of Hanoi with {num_disks} disks:\n")
towers_of_hanoi(num_disks, 'A', 'B', 'C')
