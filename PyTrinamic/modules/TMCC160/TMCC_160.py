'''
Created on 04.02.2020

@author: JM
'''
import PyTrinamic

" interfaces "
from PyTrinamic.modules.tmcl_module_interface import tmcl_module_interface
from PyTrinamic.modules.tmcl_motor_interface import tmcl_motor_interface

" features "
from PyTrinamic.modules.features.open_loop_ap_feature import open_loop_ap_feature
from PyTrinamic.modules.features.digital_hall_ap_feature import digital_hall_ap_feature
from PyTrinamic.modules.features.abn_encoder_ap_feature import abn_encoder_ap_feature
from PyTrinamic.modules.features.linear_ramp_ap_feature import linear_ramp_ap_feature
from PyTrinamic.modules.features.pid_ap_feature import pid_ap_feature
from PyTrinamic.modules.features.commutation_selection_ap_feature import commutation_selection_ap_feature

class TMCC_160(tmcl_module_interface):
    
    def __init__(self, connection, moduleID=1):
        tmcl_module_interface.__init__(self, connection, moduleID)
        self.GP = _GP

        " add the motor with available features "
        self._motors.append(TMCC_160_motor_interface(self, 0, PyTrinamic.MotorTypes.BLDC, _AP_MOTOR_0, _ENUM_MOTOR_0)) 
    
    @staticmethod
    def edsFile():
        return __file__.replace("TMCC_160.py", "TMCC160-CANopen_Hw1.00_Fw3.00.eds")
    
    def moduleName(self):
        return "TMCC-160"
        
    def moduleDescription(self):
        return "The TMCC160 is desinged for evaluating all features of the TMCC160-LC motionCookie. Voltage supply: 7 - 24"


class _AP_MOTOR_0():
    TargetPosition                 = 0
    ActualPosition                 = 1
    TargetVelocity                 = 2
    ActualVelocity                 = 3
    MaxVelocity                    = 4
    MaxTorque                      = 6
    TargetReachedVelocity          = 7
    MotorHaltedVelocity            = 9
    TargetReachedDistance          = 10
    Acceleration                   = 11
    SwitchVelocity                 = 12
    RampVelocity                   = 13
    ThermalWindingTimeConstant     = 25
    IItlimit                       = 26
    IItSum                         = 27
    IItExceededCounter             = 28
    ClearIItExceededFlag           = 29
    ReinitBldcRegulation           = 31
    PIDRegulationLoopDelay         = 133
    CurrentRegulationLoopDelay     = 134
    EnableRamp                     = 146
    ActualTorque                   = 150
    SupplyVoltage                  = 151
    DriverTemperature              = 152
    TargetTorque                   = 155
    StatusFlags                    = 156
    CommutationMode                = 159
    ClearOnNull                    = 161
    ClearOnce                      = 163
    HallOffset                     = 164
    EncoderOffset                  = 165
    TorqueP                        = 172
    TorqueI                        = 173
    singleShuntOffset              = 175
    singleShuntVref                = 176
    StartCurrent                   = 177
    DebugValue0                    = 190
    DebugValue1                    = 191
    DebugValue2                    = 192
    DebugValue3                    = 193
    DebugValue4                    = 194
    DebugValue5                    = 195
    DebugValue6                    = 196
    DebugValue7                    = 197
    DebugValue8                    = 198
    DebugValue9                    = 199
    CurrentPIDError                = 200
    CurrentPIDErrorSum             = 201
    FluxPIDError                   = 202
    FluxPIDErrorSum                = 203
    UseSingleShunt                 = 205
    dualShuntFactor                = 208
    singleShuntFactor              = 209
    ActualHallAngle                = 210
    ActualEncoderAngle             = 211
    ActualControlledAngle          = 212
    DriverDiagnosticValue          = 214
    DriverStatusAcknowledge        = 215
    DriverInitSPI                  = 216
    DriverStatusRegister2          = 217
    DriverStatusRegister3          = 218
    DriverStatusRegister4          = 219
    PositionPIDError               = 226
    VelocityPIDError               = 228
    VelocityPIDErrorSum            = 229
    PositionP                      = 230
    VelocityP                      = 234
    VelocityI                      = 235
    BrakeChopperEnabled            = 237
    BrakeChopperVoltage            = 238
    BrakeChopperHysteresis         = 239
    InitVelocity                   = 241
    InitSineDelay                  = 244
    EncoderInitMode                = 249
    EncoderSteps                   = 250
    EncoderDirection               = 251
    HallInterpolation              = 252
    MotorPoles                     = 253
    HallSensorInvert               = 254
    DriverEnabled                  = 255

class _ENUM_MOTOR_0():
    COMM_MODE_BLOCK_HALL            = 0
    COMM_MODE_FOC_HALL              = 6
    COMM_MODE_FOC_ENCODER           = 7
    COMM_MODE_FOC_CONTROLLED        = 8

    ENCODER_INIT_MODE_0             = 0
    ENCODER_INIT_MODE_1             = 1
    ENCODER_INIT_MODE_2             = 2

    FLAG_POSITION_END               = 0x00004000

class _GP():
    serialBaudRate                 = 65
    serialAddress                  = 66
    CANBitRate                     = 69
    CANsendID                      = 70
    CANreceiveID                   = 71
    telegramPauseTime              = 75
    serialHostAddress              = 76
    autoStartMode                  = 77
    CANsecondaryID                 = 83
    SerialBroadcastAddress         = 87
    applicationStatus              = 128
    programCounter                 = 130
    tickTimer                      = 132
    

class TMCC_160_motor_interface(tmcl_motor_interface):
    
    def __init__(self, parent, axisID, motorType, axisParameter, constants):
        tmcl_motor_interface.__init__(self, parent, axisID, motorType, axisParameter, constants)
        
        " add features "
        
        self.openLoop = open_loop_ap_feature(self)
        self.feature.update({"open_loop" : self.openLoop})

        self.digitalHall = digital_hall_ap_feature(self)
        self.feature.update({"digital_hall" : self.digitalHall})

        self.abnEncoder = abn_encoder_ap_feature(self)
        self.feature.update({"abn_encoder" : self.abnEncoder})

        self.linearRamp = linear_ramp_ap_feature(self)
        self.feature.update({"linear_ramp" : self.linearRamp})
        
        self.pid = pid_ap_feature(self)
        self.feature.update({"pid" : self.pid})

        self.commutationSelection = commutation_selection_ap_feature(self)
        self.feature.update({"commutation_selection" : self.commutationSelection})

    " motor type (BLDC only) "
    def setMotorType(self, motorType):
        pass
    
    def motorType(self):
        return PyTrinamic.MotorTypes.BLDC

    " motor pole pairs "
    def setMotorPolePairs(self, polePairs):
        self.setAxisParameter(self.AP.MotorPoles, polePairs*2)
 
    def motorPolePairs(self):
        return int(self.axisParameter(self.AP.MotorPoles)/2)