import subprocess


def execute(command):
    """ Executes the command on a subprocess """
    cmd = command
    print cmd
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    out, err = process.communicate()
    print out
    return out, err, process.returncode


def read_repos(repos_data):
    """ Reads a repositories.list file and returns a list of repos"""
    repos = []
    for line in repos_data:
        repos.append(line)
    return repos


def update_all(repositories):
    """ Updates each repository and returns a list of repos with new commits"""
    repositories_with_new_commits = []
    for repo in repositories:
        new_commit = update_repo(repo)
        if new_commit:
            repositories_with_new_commits.append(repo)
    return repositories_with_new_commits


def run_sonar_for(repositories):
    """ Run sonar for each repository in the list"""
    for repo in repositories:
        run_sonar(repo)


def run_sonar(repository):
    """ Run sonar for the given repository"""
    folder_name = extract_folder_name(repository)
    repo_name = extract_repo_name(repository)
    sonar_properties = "projects/" + folder_name + "/sonar-" + repo_name + ".properties"
    src_project = find_src("projects/" + folder_name + "/" + repo_name)
    out, err, rcod = execute("sonar-runner" +
                             " -Dproject.settings=" + sonar_properties +
                             " -Dsonar.sources=" + src_project)
    return out

def find_src(directory):
    import os
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if os.path.join(root, dir).endswith("app"):
                return os.path.join(root, dir)
    return "."


def clone_all(repositories):
    """ Clone all the repositories in the list"""
    new_repos = []
    execute("mkdir projects")
    for repo in repositories:
        print is_already_cloned(repo)
        if not is_already_cloned(repo):
            print clone(repo)
            config_properties(repo)
            new_repos.append(repo)
    return new_repos

def config_properties(repo):
    """
    Configures the properties of each repository
    Ensures that sonar will run correctly
    """
    folder_name = extract_folder_name(repo)
    repo_name = extract_repo_name(repo)
    properties = """
sonar.projectKey=%s
sonar.projectName=%s
sonar.projectVersion=1.0
sonar.language=java
sonar.sourceEncoding=UTF-8
    """ % (repo_name + "-" + folder_name, repo_name + "-" + folder_name)

    execute("echo '" + properties + "' > projects/" + folder_name + "/sonar-" + repo_name + ".properties")


def is_already_cloned(repository):
    """ Returns whether a repository already exists"""
    folder_name = extract_folder_name(repository)
    repo_name = extract_repo_name(repository)
    out, err, rcod = execute("ls projects | grep -x " + folder_name + " | grep -v grep")
    if out:
	out, err, rcod = execute("cd projects && cd " + folder_name + " && ls | grep -x " + repo_name + " | grep -v grep")
    return out


def clone(repository):
    """ Clones the given repository"""
    folder_name = extract_folder_name(repository)
    print execute("cd projects && mkdir -p " + folder_name)
    out, err, rcod = execute("cd projects && cd " + folder_name + " && git clone " + repository)
    return out


def update_repo(repository):
    """
    Pull the repository new commits and return True if there was new commits, False if not.
    """
    folder_name = extract_folder_name(repository)
    repo_name = extract_repo_name(repository)
    out, err, rcod = execute(
        "cd projects && cd " + folder_name + " && cd " + repo_name + " && git pull | grep \"Already up-to-date.\" | grep -v grep")
    return not out


def extract_folder_name(repository):
    """
    Extracts the folder name. Example:
    https://github.com/joopeed/sonar-repo-watcher.git
    Folder name is joopeed
    """
    return repository.split('/')[3]


def extract_repo_name(repository):
    """
    Extracts the repo name. Example:
    https://github.com/joopeed/sonar-repo-watcher.git
    Repo name is sonar-repo-watcher
    """
    return ".".join(repository.split('/')[4].split('.')[:-1])
