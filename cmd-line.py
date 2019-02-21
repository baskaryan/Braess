from simulation import simulate

theta = map(int, raw_input().split())[0]
users, resolution = map(int, raw_input().split())
search_type = raw_input().split()[0]


print simulate(theta, users, resolution, search_type)
