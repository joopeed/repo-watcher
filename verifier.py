from verify_library import *

with open('repositories.list', 'r') as repos_data:
    repositories = read_repos(repos_data)

# Try to clone all repositories if they don't exist
clone_all(repositories)

while True:
    # Pull all repositories
    repositories_with_new_commits = update_all(repositories)
    # Run sonar analysis only for repos with new commits
    run_sonar_for(repositories_with_new_commits)


