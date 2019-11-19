# AWS RoboMaker Sample Application - Open Source Rover

This sample application demonstrates and end-to-end robotics system with the Open Source Rover from NASA JPL. It includes a URDF file modeled after the popular open source project. To learn more about the open source rover, check it out [here](https://opensourcerover.jpl.nasa.gov/)

_RoboMaker sample applications include third-party software licensed under open-source licenses and is provided for demonstration purposes only. Incorporation or use of RoboMaker sample applications in connection with your production workloads or a commercial products or devices may affect your legal rights or obligations under the applicable open-source licenses. Source code information can be found [here](https://s3.console.aws.amazon.com/s3/buckets/robomaker-applications-us-east-1-72fc243f9355/hello-world/?region=us-east-1)._

## Requirements

- [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) - Other versions may work, however they have not been tested
- [Colcon](https://colcon.readthedocs.io/en/released/user/installation.html) - Used for building and bundling the application.

## Build

### Pre-build commands

```bash
sudo apt-get update
rosdep update
```

### Robot

```bash
cd robot_ws
rosws update
rosdep install --from-paths src --ignore-src -r -y
colcon build
```

### Simulation

```bash
cd simulation_ws
rosws update
rosdep install --from-paths src --ignore-src -r -y
colcon build
```

## Run

Launch the application with the following commands:

*Running Robot Application*
```bash
source robot_ws/install/local_setup.sh
roslaunch martian_detector martian_detector.launch
```

*Running Simulation Application*
```bash
source simulation_ws/install/local_setup.sh
roslaunch rover_gazebo main_with_objects.launch
```

## Using this sample with RoboMaker

You first need to install colcon-ros-bundle. Python 3.5 or above is required.

```bash
pip3 install -U setuptools
pip3 install colcon-ros-bundle
```

After colcon-ros-bundle is installed you need to build your robot or simulation, then you can bundle with:

```bash
# Bundling Robot Application
cd robot_ws
source install/local_setup.sh
colcon bundle

# Bundling Simulation Application
cd simulation_ws
source install/local_setup.sh
colcon bundle
```

This produces the artifacts `robot_ws/bundle/output.tar` and `simulation_ws/bundle/output.tar` respectively.
You'll need to upload these to an s3 bucket, then you can use these files to
[create a robot application](https://docs.aws.amazon.com/robomaker/latest/dg/create-robot-application.html),
[create a simulation application](https://docs.aws.amazon.com/robomaker/latest/dg/create-simulation-application.html),
and [create a simulation job](https://docs.aws.amazon.com/robomaker/latest/dg/create-simulation-job.html) in RoboMaker.

## ROS Nodes launched by this Sample

### Nodes created by this sample

```
/motion
/notifier
/object_detector
```


## Running the demonstration and workshop

To roam around the simulated mars world and find martians, you can use the teleop_twist_keyboard commands by running the following statement in your terminal:

```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

Full instructions on how to setup the AWS cloud infrastructure and run the demo can be found at: [https://www.robomakerworkshops.com](https://www.robomakerworkshops.com).

## License

MIT-0 - See LICENSE for further information

## How to Contribute

Create issues and pull requests against this Repository on Github
