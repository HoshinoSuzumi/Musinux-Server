# Musinux Server

## Deployment on CentOS 7

You must sure that you installed desktop environment(e.g. GNOME) on your system to use Musinux & FFmpeg.

Musinux is writen by Python3.7, so you should install that.

We have a full installation manual. Let's go.

### 1.1 Software

#### 1.1.1 FFmpeg
```shell script
# Update yum
sudo yum install epel-release -y
sudo yum update -y

# Install Nux Dextop Yum Source
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm

# Install FFmpeg
sudo yum install ffmpeg ffmpeg-devel -y

# Verify installation
ffmpeg -version
```

#### 1.1.2 Python3.7
```shell script
# Build tools
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install libffi-devel -y

# Download python
cd ~
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar -xvJf Python-3.7.0.tar.xz

# Build & Install
mkdir /usr/local/python3
cd Python-3.7.0
./configure --prefix=/usr/local/python3
make && make install

# Make soft link
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3

# Verify installation
python3 -V
pip3 -V
```

#### 1.1.3 screen
```shell script
yum install screen -y
```
---
### 1.2 Dependencies

#### 1.2.1 Get Musinux
```shell script
# Clone from GitHub 
cd ~
git clone https://github.com/boxlab/Musinux-Server.git
cd Musinux-Server
```

#### 1.2.2 Resolve dependencies
```shell script
pip3 install -r requirements.txt
```
---
### 1.3 Start server

```shell script
# Start up server on screen
screen -S Musinux python3 app.py

# Then switch to back
Ctrl A + D
```