#!/bin/bash
# Name: Atomic Archive configuration script
# Copyright Atomicorp, 2002-2022
# License: AGPL
# Credits
# 	Scott R. Shinn (atomicorp)
#	Andy Gredler  (rackspace)
#

export LANG=C
ATOMIC_VER="6.0"
VERSION="1.0-21"
SERVER=updates.atomicorp.com
#SERVER='http://52.44.51.209/'
ARCH=`uname -i`


# Input validation function
# check_input <msg> <valid responses regex> <default>
# if <default> is passed on as null, then there is no default
# Example: check_input  "Some question (yes/no) " "yes|no"  "yes"
check_input () {
  message=$1
  validate=$2
  default=$3

  while [ $? -ne 1 ]; do
    echo -n "$message "
    read INPUTTEXT < /dev/tty
    if [ "$INPUTTEXT" == "" -a "$default" != "" ]; then
      INPUTTEXT=$default
      return 1
    fi
    echo $INPUTTEXT | egrep -q "$validate" && return 1
    echo "Invalid input"
  done

}


echo
echo "Atomic Free Unsupported Archive installer, version $ATOMIC_VER"
echo
echo "BY INSTALLING THIS SOFTWARE AND BY USING ANY AND ALL SOFTWARE"
echo "PROVIDED BY ATOMICORP LIMITED YOU ACKNOWLEDGE AND AGREE:"
echo
echo "THIS SOFTWARE AND ALL SOFTWARE PROVIDED IN THIS REPOSITORY IS "
echo "PROVIDED BY ATOMICORP LIMITED AS IS, IS UNSUPPORTED AND ANY"
echo "EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE"
echo "IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR"
echo "PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ATOMICORP LIMITED, THE"
echo "COPYRIGHT OWNER OR ANY CONTRIBUTOR TO ANY AND ALL SOFTWARE PROVIDED"
echo "BY OR PUBLISHED IN THIS REPOSITORY BE LIABLE FOR ANY DIRECT,"
echo "INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES"
echo "(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS"
echo "OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)"
echo "HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,"
echo "STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)"
echo "ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED"
echo "OF THE POSSIBILITY OF SUCH DAMAGE."
echo
echo "For supported software packages please contact us at: "
echo
echo "  sales@atomicorp.com"
echo

echo
echo "Configuring the [atomic] repo archive for this system "
echo

# Detect release type
if [ -f /etc/redhat-release ]; then
        RELEASE=/etc/redhat-release
elif [ -f /etc/os-release ]; then
        RELEASE=/etc/os-release
elif [ -f /etc/openvz-release ]; then
        RELEASE=/etc/openvz-release
elif [ -f /etc/SuSE-release ]; then
        RELEASE=/etc/SuSE-release
elif [ -f /etc/os-release ]; then
        RELEASE=/etc/os-release
elif [ -f /etc/lsb-release ]; then
        RELEASE=/etc/lsb-release
elif [ -f /etc/debian_version ]; then
        RELEASE=/etc/debian_version
elif [ -f /etc/openvz-release ]; then
	RELEASE=/etc/openvz-release
elif [ -f /etc/virtuozzo-release ]; then
	RELEASE=/etc/virtuozzo-release
else
        echo "Error: unable to identify operating system"
        exit 1
fi

PKG=rpm

if grep -q "Red Hat Linux release 9  " $RELEASE ; then
  DIST="rh9"
  DIR=redhat/9
  echo
  echo "$RELEASE is no longer supported."
  echo
  exit 1
elif grep -q "Fedora Core release 2 " $RELEASE ; then
  DIST="fc2"
  DIR=fedora/2
  echo
  echo "$RELEASE is no longer supported."
  echo
  exit 1
elif grep -q "Fedora Core release 3 " $RELEASE ; then
  DIST="fc3"
  DIR=fedora/3
  echo
  echo "$RELEASE is no longer supported."
  echo
  exit 1
  #YUMDEPS="fedora-release python-elementtree python-sqlite python-urlgrabber yum"
elif grep -q "Fedora Core release 4 " $RELEASE ; then
  DIST="fc4"
  DIR=fedora/4
  echo "$RELEASE is no longer supported."
  echo
  exit 1
elif grep -q "Fedora Core release 5 " $RELEASE ; then
  DIST="fc5"
  DIR=fedora/5
  echo "$RELEASE is no longer supported."
  echo
  exit 1
elif grep -q "Fedora Core release 6 " $RELEASE ; then
  DIST="fc6"
  DIR=fedora/6
elif grep -q "Fedora release 7 " $RELEASE ; then
  DIST="fc7"
  DIR=fedora/7
elif grep -q "Fedora release 8 " $RELEASE ; then
  DIST="fc8"
  DIR=fedora/8
elif grep -q "Fedora release 9 " $RELEASE ; then
  DIST="fc9"
  DIR=fedora/9
elif grep -q "Fedora release 10 " $RELEASE ; then
  DIST="fc10"
  DIR=fedora/10
elif grep -q "Fedora release 11 " $RELEASE ; then
  DIST="fc11"
  DIR=fedora/11
elif grep -q "Fedora release 12 " $RELEASE ; then
  DIST="fc12"
  DIR=fedora/12
elif grep -q "Fedora release 13 " $RELEASE ; then
  DIST="fc13"
  DIR=fedora/13
elif grep -q "Fedora release 14 " $RELEASE ; then
  DIST="fc14"
  DIR=fedora/14
elif grep -q "Fedora release 15 " $RELEASE ; then
  DIST="fc15"
  DIR=fedora/15
elif grep -q "Fedora release 16 " $RELEASE ; then
  DIST="fc16"
  DIR=fedora/16
elif grep -q "Fedora release 17 " $RELEASE ; then
  DIST="fc17"
  DIR=fedora/17
elif grep -q "Fedora release 18 " $RELEASE ; then
  DIST="fc18"
  DIR=fedora/18
elif grep -q "Fedora release 19 " $RELEASE ; then
  DIST="fc19"
  DIR=fedora/19
elif grep -q "Fedora release 20 " $RELEASE ; then
  DIST="fc20"
  DIR=fedora/20
elif grep -q "Fedora release 21 " $RELEASE ; then
  DIST="fc21"
  DIR=fedora/21
elif grep -q "Fedora release 22 " $RELEASE ; then
  DIST="fc22"
  DIR=fedora/22
elif grep -q "Fedora release 23 " $RELEASE ; then
  DIST="fc23"
  DIR=fedora/23
elif grep -q "Fedora release 24 " $RELEASE ; then
  DIST="fc24"
  DIR=fedora/24
elif grep -q "Fedora release 25 " $RELEASE ; then
  DIST="fc25"
  DIR=fedora/25
elif grep -q "Fedora release 26 " $RELEASE ; then
  DIST="fc26"
  DIR=fedora/26
elif grep -q "Fedora release 27 " $RELEASE ; then
  DIST="fc27"
  DIR=fedora/27
elif grep -q "Fedora release 28 " $RELEASE ; then
  DIST="fc28"
  DIR=fedora/28
elif grep -q "Fedora release 29 " $RELEASE ; then
  DIST="fc29"
  DIR=fedora/29
elif grep -q "Fedora release 30 " $RELEASE ; then
  DIST="fc30"
  DIR=fedora/30
elif grep -q "Fedora release 31 " $RELEASE ; then
  DIST="fc31"
  DIR=fedora/31
elif grep -q "Fedora release 32 " $RELEASE ; then
  DIST="fc32"
  DIR=fedora/32
  VERSION="1.0-22"
elif grep -q "Fedora release 33 " $RELEASE ; then
  DIST="fc33"
  DIR=fedora/33
  VERSION="1.0-22"
elif grep -q "Fedora release 34 " $RELEASE ; then
  DIST="fc34"
  DIR=fedora/34
  VERSION="1.0-23"
elif grep -q "Fedora release 35 " $RELEASE ; then
  DIST="fc35"
  DIR=fedora/35
  VERSION="1.0-23"
elif egrep -q "Red Hat Enterprise Linux (A|E)S release 3 " $RELEASE ; then
  DIST="el3"
  DIR=redhat/3
  echo
  echo "$RELEASE is not supported at this time, you will need to configure yum manually:"
  echo "see http://$SERVER/channels for instructions"
  echo
  exit 1
elif grep -q "CentOS release 3" $RELEASE ; then
  DIST="el3"
  DIR=centos/3
  echo
  echo "$RELEASE is not supported at this time, you will need to configure yum manually:"
  echo "see http://$SERVER/channels for instructions"
  echo
  exit 1
elif egrep -q "Red Hat Enterprise Linux (A|E|W)S release 4" $RELEASE ; then
  DIST="el4"
  DIR=redhat/4
  echo "$RELEASE is not supported at this time, you will need to configure yum manually:"
  echo "see http://$SERVER/channels for instructions"
  echo
  exit 1
elif egrep -q "Red Hat Enterprise Linux.*release 5" $RELEASE ; then
  DIST="el5"
  DIR=redhat/5
elif egrep -q "Red Hat Enterprise Linux.*release 6" $RELEASE ; then
  DIST="el6"
  DIR=redhat/6
elif egrep -q "Red Hat Enterprise Linux.* 7" $RELEASE ; then
  DIST="el7"
  DIR=redhat/7
  VERSION="1.0-23"
elif egrep -q "Red Hat Enterprise Linux.* 8" $RELEASE ; then
  DIST="el8"
  DIR=redhat/8
  VERSION="1.0-23"
elif grep -q "CentOS release 3" $RELEASE ; then
  DIST="el3"
  DIR=centos/3
  echo "$RELEASE is not supported at this time, you will need to configure yum manually:"
  echo "see http://$SERVER/channels for instructions"
  echo
elif grep -q "CentOS release 4" $RELEASE ; then
  DIST="el4"
  DIR=centos/4
  echo "$RELEASE is not supported at this time, you will need to configure yum manually:"
  echo "see http://$SERVER/channels for instructions"
  echo
elif egrep -q "(release 5|release 2011)" $RELEASE ; then
  DIST="el5"
  DIR=centos/5
elif egrep -q "(release 6|release 2012)" $RELEASE ; then
  DIST="el6"
  DIR=centos/6
elif egrep -q "(release 7|release 2014)" $RELEASE ; then
  DIST="el7"
  DIR=centos/7
  VERSION="1.0-23"
elif egrep -q "(release 8|release 2019)" $RELEASE ; then
  DIST="el8"
  DIR=centos/8
  VERSION="1.0-23"
elif egrep -q "(Amazon Linux AMI|Amazon Linux 2).*" $RELEASE ; then
  DIST="amazon-2"
  DIR=amazon/2
  PKG="amazon"
elif egrep -q "(Amazon Linux AMI|Amazon)" $RELEASE ; then
  DIST="amazon-1"
  DIR=amazon/1
  PKG="amazon"
elif egrep -q "openSUSE 12" $RELEASE ; then
  DIST="suse12"
  DIR=opensuse/12
elif egrep -q "openSUSE 13" $RELEASE ; then
  DIST="suse13"
  DIR=opensuse/13
elif egrep -q "^6.0" $RELEASE ; then
  DIST="debian"
  DIR="squeeze"
  PKG=deb
elif egrep -q "wheezy" $RELEASE ; then
  DIST="debian"
  DIR="wheezy"
  PKG=deb
elif egrep -q "jessie" $RELEASE ; then
  DIST="debian"
  DIR="jessie"
  PKG=deb
elif egrep -q "stretch" $RELEASE ; then
  DIST="debian"
  DIR="stretch"
  PKG=deb
elif egrep -q "buster" $RELEASE ; then
  DIST="debian"
  DIR="buster"
  PKG=deb
elif egrep -q "bullseye" $RELEASE ; then
  DIST="debian"
  DIR="bullseye"
  PKG=deb2
elif egrep -q "lucid" $RELEASE ; then
  DIST="ubuntu"
  DIR="lucid"
  PKG=deb
elif egrep -q "precise" $RELEASE ; then
  DIST="ubuntu"
  DIR="precise"
  PKG=deb
elif egrep -q "Raring Ringtail" $RELEASE ; then
  DIST="ubuntu"
  DIR="raring"
  PKG=deb
elif egrep -q "Trusty Tahr" $RELEASE ; then
  DIST="ubuntu"
  DIR="trusty"
  PKG=deb
elif egrep -q "Xenial|Mint" $RELEASE ; then
  DIST="ubuntu"
  DIR="xenial"
  PKG=deb
elif egrep -qi "artful" $RELEASE ; then
  DIST="ubuntu"
  DIR="artful"
  PKG=deb
elif egrep -qi "bionic" $RELEASE ; then
  DIST="ubuntu"
  DIR="bionic"
  PKG=deb
elif egrep -qi "kali" $RELEASE ; then
  DIST="kali"
  DIR="kali"
  PKG=deb
elif egrep -qi "focal fossa" $RELEASE; then
  DIST="ubuntu"
  DIR="focal"
  PKG=deb2
else
  echo "Error: Unable to determine distribution type. Please send the contents of $RELEASE to support@atomicrocketturtle.com"
  exit 1
fi

# Manual for amazon
amazon_install () {

	rpm -import RPM-GPG-KEY.atomicorp.txt >/dev/null 2>&1
	rpm -import RPM-GPG-KEY.art.txt >/dev/null 2>&1

	if [ ! -f /etc/pki/rpm-gpg/RPM-GPG-KEY.atomicorp.txt ]; then
		mv /root/RPM-GPG-KEY.atomicorp.txt /etc/pki/rpm-gpg/RPM-GPG-KEY.atomicorp.txt
	fi

	if [ -f /etc/yum.repos.d/atomic.repo ]; then
		rm -f /etc/yum.repos.d/atomic.repo
	fi

	cat  << EOF > /etc/yum.repos.d/atomic.repo
[atomic]
name=Atomicorp Amazon Linux - atomic
mirrorlist=https://updates.atomicorp.com/channels/mirrorlist/atomic/$DIST-x86_64
priority=1
enabled=1
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY.atomicorp.txt
gpgcheck=1

[atomic-testing]
name=Atomicorp Amazon Linux - atomic-testing
mirrorlist=https://updates.atomicorp.com/channels/mirrorlist/atomic-testing/$DIST-x86_64
priority=1
enabled=0
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY.atomicorp.txt
gpgcheck=1


EOF

}

# RPM Distros
yum_install () {

	ATOMIC=atomic-release-$VERSION.$DIST.art.noarch.rpm

	if [ ! -f /usr/bin/yum ]; then
		echo
		echo "Error: Yum was not detected. Contact your provider for support." | tee -a $LOG
		echo
		exit 1
	fi


	if rpm -q atomic-release > /dev/null ; then
		if [ ! -f /etc/yum.repos.d/atomic.repo ]; then
			rpm -e atomic-release
		fi

	fi

	rpm -import RPM-GPG-KEY.art.txt >/dev/null 2>&1
	rpm -import RPM-GPG-KEY.atomicorp.txt >/dev/null 2>&1


    	echo -n "Downloading $ATOMIC: "
    	wget -q http://$SERVER/channels/atomic/$DIR/$ARCH/RPMS/$ATOMIC >/dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "Error: File $ATOMIC not found."
		echo
		exit
	fi

    	if [ -f $ATOMIC ]; then
      		rpm -Uvh $ATOMIC  || exit 1
      		rm -f $ATOMIC
    	else
      		echo "ERROR: $ATOMIC was not downloaded."
      		exit 1
    	fi

    	echo "OK"

	if [ ! -f /etc/yum.repos.d/atomic.repo ]; then
		echo "Error: /etc/yum.repos.d/atomic.repo was not detected."
		exit 1
	fi

	if [ ! $NON_INT ]; then
		echo
		check_input "Enable repo by default? (yes/no) [Default: yes]:" "yes|no" "yes"
		query=$INPUTTEXT
		if [ "$query" == "no" ]; then
			sed -i 's/enabled = 1/enabled = 0/' /etc/yum.repos.d/atomic.repo
		fi

	fi

}

apt_install_2 () {
	APT_SOURCES="/etc/apt/sources.list.d/atomic.list"
	ARCH=$(dpkg --print-architecture)

	# GPG dependency
	if [ ! -f /usr/bin/gpg ]; then
		/usr/bin/apt-get update
        	/usr/bin/apt-get -y --force-yes install gpg
	fi
        wget -O -  https://www.atomicorp.com/RPM-GPG-KEY.atomicorp.txt | apt-key add -
        if [ $? -ne 0 ]; then
                echo
                echo "Error: Installation failed"
                echo
                exit 1
        fi

	echo -n "Adding [atomic] to $APT_SOURCES: "
        echo "deb [trusted=yes] https://updates.atomicorp.com/channels/atomic/${DIST} ${DIR}/${ARCH}/ " > $APT_SOURCES
	echo "OK"


}

# DEB Distros (Legacy repo)
apt_install () {

        /usr/bin/apt-get update

        /usr/bin/apt-get -y --force-yes install gpg

        wget -O -  https://www.atomicorp.com/RPM-GPG-KEY.atomicorp.txt | apt-key add -
        if [ $? -ne 0 ]; then
                echo
                echo "Error: Installation failed"
                echo
                exit 1
        fi


	if [ -d /etc/apt/sources.list.d/ ]; then
		APT_SOURCES="/etc/apt/sources.list.d/atomic.list"

		echo -n "Adding [atomic] to $APT_SOURCES: "
		if [ ! -f $APT_SOURCES ]; then
			echo "deb https://updates.atomicorp.com/channels/atomic/$DIST $DIR main" > $APT_SOURCES
			echo "OK"
		else
			echo "Already installed"
		fi

	else
		APT_SOURCES="/etc/apt/sources.list"
		echo -n "Adding [atomic] to $APT_SOURCES: "
		if ! grep -q "atomic/$DIST $DIR" $APT_SOURCES ; then
			echo "deb https://updates.atomicorp.com/channels/atomic/$DIST $DIR main" >> /etc/apt/sources.list
			echo "OK"
		else
			echo "Already installed"
		fi
	fi


}


# Installation


# GPG Keys
echo -n "Installing the Atomic GPG keys: "
if [ ! -f RPM-GPG-KEY.art.txt ]; then
  wget -q https://www.atomicorp.com/RPM-GPG-KEY.art.txt 1>/dev/null 2>&1
fi

if [ ! -f RPM-GPG-KEY.atomicorp.txt ]; then
  wget -q https://www.atomicorp.com/RPM-GPG-KEY.atomicorp.txt 1>/dev/null 2>&1
fi
echo "OK"
echo

if [ "$PKG" == "rpm" ]; then
	yum_install
elif [ "$PKG" == "deb" ]; then
	apt_install
elif [ "$PKG" == "deb2" ]; then
	apt_install_2
elif [ "$PKG" == "amazon" ]; then
	amazon_install

fi

echo
echo
echo "The Atomic repo has now been installed and configured for your system"
echo "The following channels are available:"
echo "  atomic          - [ACTIVATED] - contains the stable tree of ART packages"
echo "  atomic-testing  - [DISABLED]  - contains the testing tree of ART packages"
echo "  atomic-bleeding - [DISABLED]  - contains the development tree of ART packages"
echo
echo
