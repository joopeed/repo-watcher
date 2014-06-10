import subprocess

def execute(command):
        # Executes the command on a subprocess
        cmd = command
        process = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, err = process.communicate()
        return out, err, process.returncode

def read_repos(repos_data):
    repos = []
    for line in repos_data:
           repos = line
    return repos

def update_all(repositories):
    repositories_with_new_commits = []
    for repo in repositories:
        new_commit = update_repo(repo)
        if new_commit:
            repositories_with_new_commits.append(repo)
    return repositories_with_new_commits

def run_sonar_for(repositories):
    for repo in repositories:
        run_sonar(repo)

def run_sonar(repository):
    folder_name = extract_folder_name(repository)
    out, err, rcod = execute("cd "+folder_name+" | cd "+repo_name+" | sonar_runner")
    return out

def clone_all(repositories):
    for repo in repositories:
        if not is_already_cloned(repo):
            clone(repo)

def is_already_cloned(repository):
    folder_name = extract_folder_name(repository)
    out, err, rcod = execute("ls | grep "+folder_name+" | grep -v grep")
    return not not out

def clone(repository):
    folder_name = extract_folder_name(repository)
    execute("mkdir "+folder_name)
    out, err, rcod = execute("cd "+ folder_name +" | git clone " + repository)
    return out

def update_repo(repository):
    """
    Pull the repository new commits and return True if there was new commits, False if not.
    """
    folder_name = extract_folder_name(repository)
    repo_name = extract_repo_name(repository)
    out, err, rcod = execute("cd "+folder_name+" | cd "+repo_name+" | git pull | grep \"Already up-to-date.\" | grep -v grep")
    return not out

def extract_folder_name(repository):
    return repository.split('/')[3]

def extract_repo_name(repository):
    return repository.split('/')[4].split('.')[0]
