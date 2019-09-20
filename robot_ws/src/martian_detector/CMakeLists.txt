################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(martian_detector)

## Add support for C++11, supported in ROS Kinetic and newer
add_definitions(-std=c++11)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
)


################################################################################
# Setup for python modules and scripts
################################################################################
catkin_python_setup()

################################################################################
# Declare ROS messages, services and actions
################################################################################

## Generate messages in the 'msg' folder
#add_message_files(
#  FILES
#  TurnCommand.msg
#)

################################################################################
# Declare ROS dynamic reconfigure parameters
################################################################################

################################################################################
# Declare catkin specific configuration to be passed to dependent projects
################################################################################
catkin_package(
  DEPENDS
    roscpp
    rospy
)

################################################################################
# Build
################################################################################
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} )

################################################################################
# Install
################################################################################

catkin_install_python(PROGRAMS
  nodes/notifier
  nodes/object_detector
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

foreach(dir launch)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
