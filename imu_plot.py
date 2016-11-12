#!/usr/bin/env python

import rosbag
from tf.transformations import euler_from_quaternion
import matplotlib
import matplotlib.pyplot as plt


class ErrorAnalysis(object):
    def __init__(self, path_to_bag, topic):
        self.bag_name = path_to_bag.split('/')[-1]
        self.bag = rosbag.Bag(path_to_bag)
        self.topic = topic

    def parse_bag_file(self):
        self.t = []
        self.orientations = []
        for topic, msg, time_stamp in self.bag.read_messages(topics=[self.topic]):
            if topic == self.topic:
                self.t.append(time_stamp)
                if topic == '/imu/data' or '/jackal/imu/data':
                    orientation = msg.orientation
                elif topic == '/jackal_velocity_controller/odom' or '/odometry/filtered':
                    orientation = msg.pose.pose.orientation
                self.orientations.append(orientation)
        self.bag.close()

    def plot(self):
        yaws = [euler_from_quaternion((orientation.x, orientation.y, orientation.z, orientation.w))[2] for orientation in self.orientations]
        t = [elem.to_sec() for elem in self.t]
        fig = plt.figure()
        fig.suptitle(self.bag_name + ' : ' + self.topic, fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('t [sec]')
        ax.set_ylabel('yaw [radians]')
        plt.plot(t, yaws, 'r--')
        plt.show()



if __name__ == '__main__':

    ea = ErrorAnalysis('/home/omer/bags/straight_line_gazebo_6.bag', '/jackal/imu/data')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/291016/jackal_14_straight_line_programmed.bag', '/odometry/filtered')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/291016/jackal_14_straight_line_programmed.bag', '/odometry/filtered')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/291016/jackal13_straight_driving_programmed.bag', '/odometry/filtered')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle.bag', '/imu/data')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle.bag', '/odometry/filtered')

    # ea = ErrorAnalysis('/home/cear/bags/jackal_native/291016/jackal_14_straight_line_programmed_2.bag', '/imu/data')
    # ea = ErrorAnalysis('/home/cear/bags/jackal_native/291016/jackal13_straight_driving_programmed_2.bag', '/imu/data')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle_small.bag', '/imu/data')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle_small.bag', '/odometry/filtered')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/straight_line_programmed.bag', '/imu/data')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/straight_line_programmed.bag', '/odometry/filtered')

    ea.parse_bag_file()
    ea.plot()
