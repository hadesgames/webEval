from fabric.api import env, run, sudo, local

def production():
	env.hosts = ['webEval@webEval.no-ip.org']
	env.user = 'webEval'

def reboot_nginx():
    "Reboot nginx server."
    sudo("/etc/init.d/nginx restart", pty=True)

def reboot_apache():
    "Reboot apache server."
    sudo("/etc/init.d/httpd reload", pty=True)

def git_pull():
    "Updates the repository."
    run("cd ~/work/webEval/; git pull")

def db_migrate():
    "Migrates the database."
    run("cd ~/work/webEval/; ./manage.py migrate")

def deploy():
    git_pull()
    db_migrate()
    reboot_apache()
    reboot_nginx()
