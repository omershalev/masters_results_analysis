#!/usr/bin/env python

import rosbag
from tf.transformations import euler_from_quaternion
import matplotlib
import matplotlib.pyplot as plt

def interpolate(vector):
    previous = next(item for item in vector if item != None)
    for idx in range(0, len(vector)):
        current = vector[idx]
        if current == None:
            vector[idx] = previous
        else:
            previous = current
    return vector
        # TODO: should we do linear interpolation?


class ErrorAnalysis(object):
    def __init__(self, path_to_bag, topic):
        self.bag_name = path_to_bag.split('/')[-1]
        self.bag = rosbag.Bag(path_to_bag)
        self.topic = topic

    def parse_bag_file(self):
        self.t = []
        self.positions = []
        for topic, msg, time_stamp in self.bag.read_messages(topics=[self.topic]):
            if topic == self.topic:
                self.t.append(time_stamp)
                position = msg.pose.pose.position
                self.positions.append(position)
        self.bag.close()

    def plot_x(self):
        x = [position.x for position in self.positions]
        t = [elem.to_sec() for elem in self.t]
        fig = plt.figure()
        fig.suptitle(self.bag_name + ' : ' + self.topic, fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('t [sec]')
        ax.set_ylabel('x [m]')
        plt.plot(t, x, 'r--')
        plt.show()

    def plot_y(self):
        y = [position.y for position in self.positions]
        t = [elem.to_sec() for elem in self.t]
        fig = plt.figure()
        fig.suptitle(self.bag_name + ' : ' + self.topic, fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.set_xlabel('t [sec]')
        ax.set_ylabel('y [m]')
        plt.plot(t, y, 'b--')
        plt.show()


if __name__ == '__main__':


    # ea = ErrorAnalysis('/home/omer/bags/straight_line_gazebo_7.bag', '/jackal/jackal_velocity_controller/odom')
    ea = ErrorAnalysis('/home/omer/bags/straight_line_gazebo_7.bag', '/jackal/odometry/filtered')


    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/291016/jackal_14_straight_line_programmed.bag', '/odometry/filtered')

    # ea = ErrorAnalysis('/home/cear/bags/jackal_native/291016/jackal13_straight_driving_programmed_2.bag', '/jackal_velocity_controller/odom')
    # ea = ErrorAnalysis('/home/cear/bags/jackal_native/291016/jackal13_straight_driving_programmed_2.bag', '/odometry/filtered')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle.bag', '/odometry/filtered')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle.bag', '/jackal_velocity_controller/odom')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle_small.bag', '/odometry/filtered')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/rectangle_small.bag', '/jackal_velocity_controller/odom')

    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/straight_line_programmed.bag', '/odometry/filtered')
    # ea = ErrorAnalysis('/home/omer/orchard_navigation_data/jackal_native/straight_line_programmed.bag', '/jackal_velocity_controller/odom')
    

    ea.parse_bag_file()
    ea.plot_x()
    ea.plot_y()
