# Development Environment Setup

## 1. Operating System & Prerequisites
- **OS**: Ubuntu 22.04 LTS (Jammy Jellyfish) x86_64.
- **Root Permissions**: Sudo access required for package installation.

## 2. Base Toolchain Installation
```bash
sudo apt update && sudo apt install -y \
    build-essential \
    cmake \
    git \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    python3-vcstool \
    clang-format \
    flake8 \
    black
```

## 3. ROS 2 Humble Installation
Ensure ROS 2 Humble Hawksbill desktop is installed:
```bash
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update && sudo apt install -y ros-humble-desktop
```

## 4. Gazebo Sim (Harmonic / Garden) & Nav2
For ROS 2 Humble with Gazebo Harmonic (8.15.0+):
```bash
sudo apt install -y \
    ros-humble-ros-gzharmonic \
    ros-humble-ros-gzharmonic-sim \
    ros-humble-ros-gzharmonic-bridge \
    ros-humble-gz-ros2-control \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-robot-localization \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers
```

## 5. Eclipse Zenoh Installation
```bash
echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null
sudo apt update && sudo apt install -y zenoh zenoh-bridge-dds
pip3 install eclipse-zenoh
```
