#pragma once
#ifndef _MOTOR_COM_H_
#define _MOTOR_COM_H_

#define COM_INST    com[0]
#define COM_FUNC    com[1]
#define COM_ID      com[2]
#define COM_DATA    com[3]
#define COM_DATA2   com[4]

#define MOTOR_INST_PING             'P'
#define MOTOR_INST_READ             'R'
#define MOTOR_INST_WRITE            'W'
#define MOTOR_INST_REG_WRITE        'G'
#define MOTOR_INST_ACTION           'A'
#define MOTOR_INST_RESET            'E'
#define MOTOR_INST_SYNC_WRITE       'S'
#define MOTOR_INST_ACK              'K'
#define MOTOR_INST_INFO             '-'
#define MOTOR_INST_WARN             '~'
#define MOTOR_INST_FATAL            '!'
#define MOTOR_END_CHAR				'\r\n'

#define MOTOR_FUNC_POSITION         'P'
#define MOTOR_FUNC_SPEED            'S'
#define MOTOR_FUNC_LOAD             'L'
#define MOTOR_FUNC_VOLTAGE          'V'
#define MOTOR_FUNC_TEMPERATURE      'T'
#define MOTOR_FUNC_TORQUE           'Q'

////
#define CTR_DLC                       '*'

//control msg INST FUNC ID DATA
//motor   msg INST FUNC ID DATA
/*
#define CONTROL_INST_PING             'P'
#define CONTROL_INST_READ             'R'
#define CONTROL_INST_WRITE            'W'
#define CONTROL_INST_REG_WRITE        'G'
#define CONTROL_INST_ACTION           'A'
#define CONTROL_INST_RESET            'E'
#define CONTROL_INST_SYNC_WRITE       'S'
*/
#define CONTROL_INST_SET              'S'
#define CONTROL_INST_GET              'G'
#define CONTROL_INST_INFO             '-'
#define CONTROL_INST_WARN             '~'
#define CONTROL_INST_FATAL            '!'

#define CONTROL_FUNC_POSITION         'P'
#define CONTROL_FUNC_SPEED            'S'
#define CONTROL_FUNC_LOAD             'L'
#define CONTROL_FUNC_VOLTAGE          'V'
#define CONTROL_FUNC_TEMPERATURE      'T'
#define CONTROL_FUNC_TORQUE           'Q'

#define CONTROL_FUNC_POSITION_HARD         'Z'
#define CONTROL_FUNC_POSITION_SOFT         'X'

#endif
