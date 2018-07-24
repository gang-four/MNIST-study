from pymultiwii import MultiWii
import struct
import time

serialPort = "/dev/tty.usbmodem1411"
board = MultiWii(serialPort)
while True :
    # print board.sendCMD(4,MultiWii.SET_RAW_RC,[1500,1500,1500,1599])  #MSP_SET_RAW_RC
    print board.getData(MultiWii.STATUS)
    print board.getData(MultiWii.RAW_IMU)
    print board.getData(MultiWii.ATTITUDE)
    print board.getData(MultiWii.ALTITUDE)
    print board.getData(MultiWii.MOTOR)
    print board.getData(MultiWii.RC)
    print board.getData(MultiWii.ANALOG)

    print board.getData(MultiWii.RC_TUNING)
    print board.getData(MultiWii.DEBUG)
    # board.arm()
#
# board.sendCMD(8,214,[1500])
# data = [1000,2000]
# checksum = 0
# total_data = ['$', 'M', '<', 100, 214] + data
# for i in struct.pack('<2B%dH' % len(data), *total_data[3:len(total_data)]):
#     checksum = checksum ^ ord(i)
#     print checksum
# total_data.append(checksum)
# print total_data
# print len(data)
#
# while True:
#
#     timer = 0
#     start = time.time()
#     print timer
#     while timer < 0.5:
#         data = [1500,1500,2000,1000,1500,1500,2000,1000]
#         board.sendCMD(8,MultiWii.SET_RAW_RC,data)
#         time.sleep(0.05)
#         timer = timer + (time.time() - start)
#         print timer
#         start =  time.time()