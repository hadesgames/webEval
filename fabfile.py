def production():
    config.fab_hosts = ['webEval.no-ip.org']
    config.repos = (('webEval','origin','master'))

def reboot_apache():
    "Reboot Apache2 server."
    run("sudo /etc/init.d/httpd reload")

def git_reset():
    "Resets the repository to specified version."
    run("cd ~/work/webEval/; git reset --hard")

def git_pull():
    "Updates the repository."
    run("cd ~/work/webEval/; git pull")

def git_commit():
    "Commits the source code."
    local("git commit")

def git_push():
    "Pushes the source code."
    local("git push")

def deploy():
    git_commit()
    git_push()
    git_pull()
    reboot_apache()
