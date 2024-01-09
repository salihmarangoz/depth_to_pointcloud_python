# depth_to_pointcloud_python

![screenshot](screenshot.png)

I couldn't find a Python implementation of ROS `image_pipeline`, for depth to pointcloud conversion using pinhole camera model. Alternatively, Open3D can be used, but I couldn't find a way to do the conversion and keeping the data structure organized.

So, this implementation does the same thing as the `convert` function implemented [here](https://github.com/ros-perception/image_pipeline/blob/noetic/depth_image_proc/include/depth_image_proc/depth_conversions.h). Just copy the function in `depth_to_pointcloud.py` and use it. Features:

- Handles 16 bit unsigned integer depth input.
- Handles 16/32/64 bit floating point depth input.
- Only numpy dependency.