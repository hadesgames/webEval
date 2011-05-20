all:
	exit
	git clone http://github.com/sciyoshi/pyfacebook.git
	cd pyfacebook; sudo python setup.py install; cd ..
