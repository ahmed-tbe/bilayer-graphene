from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

file_path = "bonds.reax"
BOND_ORDER_CUTOFF = 0.9
CARBON_TYPE = 1

interlayer_bond_counts = defaultdict(int)

def process_timestep(timestep, atoms):
    """Counts atoms with 4 C–C bonds at a given timestep."""
    id_type_map = {int(a[0]): int(a[1]) for a in atoms}
    carbon_neighbors = defaultdict(list)

    for a in atoms:
        atom_id = int(a[0])
        atom_type = int(a[1])
        num_neighbors = int(a[2])

        if atom_type != CARBON_TYPE or num_neighbors < 4:
            continue

        neighbor_ids = list(map(int, a[3:3 + num_neighbors]))
        bond_orders = list(map(float, a[3 + num_neighbors + 1 : 3 + num_neighbors + 1 + num_neighbors]))

        valid_carbon_bonds = [
            neighbor_id for neighbor_id, bond_order in zip(neighbor_ids, bond_orders)
            if bond_order > BOND_ORDER_CUTOFF and id_type_map.get(neighbor_id) == CARBON_TYPE
        ]

        if len(valid_carbon_bonds) == 4:
            # Count this as an interlayer C–C bonded atom
            carbon_neighbors[atom_id] = valid_carbon_bonds
            # Print bond order values for debug/analysis
            print(f"Timestep {timestep} - Atom {atom_id} has C–C bonds with:")
            for neighbor_id, bond_order in zip(neighbor_ids, bond_orders):
                if bond_order > BOND_ORDER_CUTOFF and id_type_map.get(neighbor_id) == CARBON_TYPE:
                    print(f"   → Atom {neighbor_id} | Bond Order = {bond_order:.3f}")

    interlayer_bond_counts[timestep] = len(carbon_neighbors)

timestep = None
atoms = []

# --- Read bonds.reax ---
with open(file_path, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("# Timestep"):
            if timestep is not None:
                process_timestep(timestep, atoms)
            timestep = int(line.split()[-1])
            atoms = []
        elif not line.startswith("#"):
            split_line = line.split()
            if len(split_line) < 3:
                print(f"⚠️ Unexpected line format at timestep {timestep}: {line}")
                continue
            atoms.append(split_line)


# Process final timestep
if timestep is not None:
    process_timestep(timestep, atoms)

# --- Plot ---
sorted_timesteps = sorted(interlayer_bond_counts.keys())
bond_values = [interlayer_bond_counts[ts] for ts in sorted_timesteps]

plt.figure(figsize=(10, 5))
plt.plot(sorted_timesteps, bond_values, linestyle='-', color='darkred')
plt.xlabel("Timestep")
plt.ylabel("Number of 4-Bonded C–C Atoms")
plt.title("C–C Interlayer Bonding Over Time")
plt.grid(True)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
#plt.show()
plt.savefig("cc_bonds_over_time.png")