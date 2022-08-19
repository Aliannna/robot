# from time import sleep
# from picamera import PiCamera

# camera = PiCamera()
# camera.resolution = (1024, 768)
# camera.start_preview()
# # Camera warm-up time
# sleep(2)
# camera.capture('foo.jpg')

# import time, board,22!4

import time

import adafruit_vl53l0x

import dual_VL53L0X

(vl530, vl531) = dual_VL53L0X.setup(25, 24)
vl530.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# Main loop will read the range and print it every second.
while True:
    print("Range 1: {0}mm\t".format(vl530.range),
          "Range 2: {0}mm".format(vl531.range))
    time.sleep(1.0)

# while True:
#     time.sleep(0.1)
#     if (not (vl53.range < 1000 and vl53.range - dists[-1] < 500)) \
#         and dists[-1] > 0:
#         print("Rejecting: {0}mm".format(vl53.range))
#         d.set_effort(0.7 * SPEED)
#         d.set_theta_effort(0.3)
#         continue

#     d.set_effort(SPEED)
#     dists.pop()
#     dists = [vl53.range] + dists
#     dist = np.average(dists)

#     # robot direction controller (PI controller) --

#     # propotion term
#     theta_effort = max(min(KP * (DIST_SP - dist) + 0.5 + ss, 1.0), 0.0)

#     # integral term
#     ss += KI * (DIST_SP - dist)
#     # ----------------------------------------------

#     d.set_theta_effort(theta_effort)


#     print("Range: {0}mm".format(vl53.range))
#     print("Effort: {0}".format(theta_effort))