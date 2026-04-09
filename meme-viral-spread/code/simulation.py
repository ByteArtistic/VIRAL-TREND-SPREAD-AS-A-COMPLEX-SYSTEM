import numpy as np
import random
import matplotlib.pyplot as plt

# -----------------------------
# PARAMETERS (you can tweak these)
# -----------------------------
num_users = 200       # total number of users (nodes)
avg_connections = 5  # approx number of connections per user
p = 0.2                # base probability of sharing
num_runs = 200         # number of simulations

# -----------------------------
# STEP 1: CREATE NETWORK
# -----------------------------
# Graph is stored as a dictionary:
# key = user, value = set of connected users

graph = {}

for i in range(num_users):
    graph[i] = set()

# randomly assign connections
for i in range(num_users):
    while len(graph[i]) < avg_connections:
        j = random.randint(0, num_users - 1)

        # avoid self-loop
        if j != i:
            graph[i].add(j)
            graph[j].add(i)   # make connection bidirectional

# -----------------------------
# FUNCTION: SINGLE SIMULATION
# -----------------------------
def run_simulation():

    # pick one random user to start meme
    start = random.randint(0, num_users - 1)

    active_users = set([start])   # users who just shared
    visited = set([start])        # all users who have ever shared

    # loop until no new users become active
    while len(active_users) > 0:

        new_active = set()   # users who will share in next step

        # go through all currently active users
        for user in active_users:

            # check all neighbors
            for neighbor in graph[user]:

                # if neighbor has not already shared
                if neighbor not in visited:

                    # count how many of neighbor's friends are active
                    active_neighbors = 0
                    for x in graph[neighbor]:
                        if x in active_users:
                            active_neighbors += 1

                    # ensure at least 1 influence
                    m = max(1, active_neighbors)

                    # probability increases with more active neighbors
                    prob = 1 - (1 - p) ** m

                    # decide if neighbor shares
                    if random.random() < prob:
                        new_active.add(neighbor)
                        visited.add(neighbor)

        # update active users for next step
        active_users = new_active

    # return total number of users who shared (avalanche size)
    return len(visited)

# -----------------------------
# STEP 2: RUN MULTIPLE SIMULATIONS
# -----------------------------
avalanche_sizes = []

for i in range(num_runs):
    size = run_simulation()
    avalanche_sizes.append(size)

# -----------------------------
# STEP 3: PLOT NORMAL HISTOGRAM
# -----------------------------
plt.figure()
plt.hist(avalanche_sizes, bins=20)
plt.xlabel("Avalanche Size (Number of Users)")
plt.ylabel("Frequency")
plt.title("Distribution of Meme Spread")
plt.show()

# -----------------------------
# STEP 4: LOG-LOG PLOT
# -----------------------------
hist, bins = np.histogram(avalanche_sizes, bins=20)

# avoid zeros for log scale
bins = bins[:-1]
hist = hist + 1  # avoid log(0)

plt.figure()
plt.loglog(bins, hist, 'o')
plt.xlabel("Avalanche Size (log scale)")
plt.ylabel("Frequency (log scale)")
plt.title("Log-Log Plot of Avalanche Distribution")
plt.show()