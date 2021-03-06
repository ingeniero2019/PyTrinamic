'''
Move a motor in CST mode with CANopen using the TMCM-1636 module

Created on 15.05.2020

@author: JM
'''

if __name__ == '__main__':
    pass

import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM1636.TMCM_1636 import TMCM_1636
import time

PyTrinamic.showInfo()

" choose the right bustype before starting the script "
connectionManager = ConnectionManager(" --interface kvaser_CANopen", connectionType = "CANopen")
network = connectionManager.connect()

node = network.addDs402Node(TMCM_1636.getEdsFile(), 1)
module = node

" this function initializes the DS402 state machine "
node.setup_402_state_machine()

" communication area "
objManufacturerDeviceName      = module.sdo[0x1008]
objManufacturerHardwareVersion = module.sdo[0x1009]

print()
print("Module name:        %s" % objManufacturerDeviceName.raw)
print("Hardware version:   %s" % objManufacturerHardwareVersion.raw)

" manufacturer specific area "
objMaximumCurrent             = module.sdo[0x2003]
objSwitchParameter            = module.sdo[0x2005]
objCommutationMode            = module.sdo[0x2055]
objMotorPolePairs             = module.sdo[0x2056]

" encoder settings "
objEncoderDirection           = module.sdo[0x2080][1]
objEncoderSteps               = module.sdo[0x2080][2]
objEncoderInitMode            = module.sdo[0x2080][3]

" profile specific area "
objControlWord              = module.sdo[0x6040]
objStatusWord               = module.sdo[0x6041]
objModeOfOperation          = module.sdo[0x6060]
objActualPosition           = module.sdo[0x6064]
objTargetTorque             = module.sdo[0x6071]
objTargetPosition           = module.sdo[0x607A]
objAcceleration             = module.sdo[0x6083]
objActualVelocity           = module.sdo[0x606C]
objDesiredVelocity          = module.sdo[0x60FF]
objVelocityActualValue      = module.sdo[0x606C]

"""
    Define all motor configurations for the TMCM-1636.

    The configuration is based on our standard BLDC motor (QBL4208-61-04-013-1024-AT).
    If you use a different motor be sure you have the right configuration setup otherwise the script may not work.
"""
objMotorPolePairs.raw              = 4
objMaximumCurrent.raw              = 1500
objCommutationMode.raw             = 3
objEncoderSteps.raw                = 4096
objEncoderDirection.raw            = 1
print("MotorPoles:               %d" % objMotorPolePairs.raw)
print("CommutationMode:          %d" % objCommutationMode.raw)
print("Encoder_StepsPerRotation: %d" % objEncoderSteps.raw)
print("Encoder_Direction:        %d" % objEncoderDirection.raw)
print()

" reset node from fault and set it to Operation Enable state "
node.reset_from_fault() 

def startCST():

    print("Node state before switcHParameter write:" + node.state)
    objSwitchParameter.raw = 3

    timeout = time.time() + 15
    node.state = 'READY TO SWITCH ON'
    while node.state != 'READY TO SWITCH ON':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    timeout = time.time() + 15
    node.state = 'SWITCHED ON'
    while node.state != 'SWITCHED ON':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    if objModeOfOperation.raw != 10:
        objModeOfOperation.raw = 10
    print("MODE OF OPERATION SET TO: %d" % objModeOfOperation.raw)

    timeout = time.time() + 15
    node.state = 'OPERATION ENABLED'
    while node.state != 'OPERATION ENABLED':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    return

startCST()

" set target torque (positive direction)"
objTargetTorque.raw = 1000
print("\nTarget torque: " + str(objTargetTorque.raw))
time.sleep(3)

" set target torque (negative direction)"
objTargetTorque.raw = -1000
print("Target torque: " + str(objTargetTorque.raw))
time.sleep(3)

" reset target torque"
objTargetTorque.raw = 0
print("Target torque: " + str(objTargetTorque.raw))

network.close()
print("Ready.")
