from fabric.api import env, run, sudo, local

def production():
	env.hosts = ['webEval@webEval.no-ip.org']
	env.user = 'webEval'

def reboot_nginx():
    "Reboot Apache2 server."
    sudo("/etc/init.d/nginx restart", pty=True)

def reboot_fastcgi():
	"Reboot FastCGI server."
	run("~/work/webEval/webEvald")

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
    reboot_nginx()
    reboot_fastcgi
