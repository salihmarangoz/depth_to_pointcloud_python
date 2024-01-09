
import numpy as np

def depth_to_pointcloud(depth_image, cx, cy, fx, fy, max_depth=None):
  """Convert depth image to pointcloud. See: https://ros.org/reps/rep-0118.html
     Note: This package does not handle negative floating point inputs.

  Args:
      depth_image (numpy.ndarray): Depth image with (height, width) shape and numpy.uint16 or numpy.float dtype
      cx (float): Camera parameter.
      cy (float): Camera parameter.
      fx (float): Camera parameter.
      fy (float): Camera parameter.
      max_depth  (float): Assigns NaN value to points exceeding the maximum depth. In meters.

  Returns:
      numpy.ndarray: Pointcloud with shape (3, height, width)
  """
  u,v = np.meshgrid(np.arange(0, depth_image.shape[1]), np.arange(0, depth_image.shape[0]), sparse=True)

  if np.issubdtype(depth_image.dtype, np.uint16):
    nan_mask = depth_image == 0
    depth_image = depth_image.astype(np.float32) / 1000.0
    depth_image[nan_mask] = np.nan

  if max_depth is not None:
    max_depth_mask = depth_image > max_depth
    depth_image[max_depth_mask] = np.nan

  px = (u - cx) * depth_image / fx
  py = (v - cy) * depth_image / fy
  pz = depth_image
  return np.stack([px,py,pz], axis=0).copy()

# Example code
if __name__ == "__main__":

  # Read Data
  import cv2
  cx, cy, fx, fy = 319.55487061, 187.6280365, 452.25476074, 452.47180176
  color_image = cv2.cvtColor(cv2.imread('color_image.png', cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)/255 # shape: (360, 640, 3)
  depth_image = cv2.imread('depth_image.png', cv2.IMREAD_ANYDEPTH) # shape: (360, 640)

  # Depth to Pointcloud
  pointcloud = depth_to_pointcloud(depth_image, cx, cy, fx, fy, max_depth=1.0) # organized. shape: (3, 360, 640)

  # Filter Pointcloud from NaN values
  finite_mask = np.isfinite(pointcloud.sum(axis=0)) # shape: (360, 640)
  pointcloud_filtered = pointcloud[:,finite_mask].copy() # not-organized. shape: (3, 121982)
  color_image_filtered = np.moveaxis(color_image, 2, 0)[:, finite_mask].copy() # shape: (3, 121982)

  # Visualization
  import open3d as o3d
  pcd = o3d.geometry.PointCloud()
  pcd.points = o3d.utility.Vector3dVector(pointcloud_filtered.T.reshape((-1,3)))
  pcd.colors = o3d.utility.Vector3dVector(color_image_filtered.T.reshape((-1,3)))
  o3d.visualization.draw_geometries([pcd])