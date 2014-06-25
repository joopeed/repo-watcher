from verify_library import *
print 'Opening repositories list...'
with open('repositories.list', 'r') as repos_data:
    repositories = read_repos(repos_data)
print 'Done!'
print 'Cloning all repositories list'
# Try to clone all repositories if they don't exist
clone_all(repositories)
print 'Done!'
while True:
    print 'Updating repos...'
    # Pull all repositories
    repositories_with_new_commits = update_all(repositories)
    # Run sonar analysis only for repos with new commits
    print 'Rerunning sonar for certain repos...(if necessary)'
    run_sonar_for(repositories_with_new_commits)


