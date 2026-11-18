# Build Instructions

## 1. Workspace Configuration
Source the ROS 2 Humble setup script:
```bash
source /opt/ros/humble/setup.bash
cd /home/oem/repository
```

## 2. Dependency Resolution
Resolve all upstream package dependencies using `rosdep`:
```bash
sudo rosdep init 2>/dev/null || true
rosdep update
rosdep install --from-paths src interfaces --ignore-src -r -y
```

## 3. Building the Workspace
Build with symlink installation for faster Python development iteration:
```bash
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

## 4. Sourcing the Workspace
```bash
source /home/oem/repository/install/setup.bash
```
