import time


class JunDuoGripper:
    def __init__(self, arm, gripper_force: int = 255, gripper_v: int = 255):
        """
        初始化夹爪
        :param arm: 睿尔曼机械臂对象，因为主要是靠写寄存器实现操作交互
        :param gripper_force: 预设夹爪的力，值为 0 - 255 之间
        :param gripper_v: 预设夹爪的速度，值为 0 - 255 之间
        """
        self.arm = arm
        # 设置夹爪的力
        self.gripper_force = gripper_force
        # 设置夹爪的速度
        self.gripper_v = gripper_v
        # 设置电压
        self.arm.Set_Tool_Voltage(3)
        # 设置写寄存器模式
        self.arm.Set_Modbus_Mode(1, 115200, 1, True)
        # 激活夹爪
        self.arm.Write_Registers(1, 1000, 1, [0, 0], 9, True)
        # 使能夹爪
        self.arm.Write_Registers(1, 1000, 1, [0, 1], 9, True)
        # 打开夹爪
        self.arm.Write_Registers(1, 1000, 3, [0, 9, 255, 0, self.gripper_force, self.gripper_v], 9)

    def set_gripper_v(self, gripper_v):
        """
        修改夹爪的速度
        :param gripper_v: 夹爪的速度，值为 0 - 255 之间
        """
        self.gripper_v = gripper_v

    def set_gripper_force(self, gripper_force):
        """
        修改夹爪的力
        :param gripper_force: 夹爪的力，值为 0 - 255 之间
        """
        self.gripper_force = gripper_force

    def gripper_close(self, wait_time: int = 2):
        """
        夹爪闭合
        :param wait_time: 夹爪闭合期间为非阻塞形式，为避免夹爪尚未闭合就出现下一步操作的情况，手动增加延时
        """
        # 关闭夹爪
        self.arm.Write_Registers(1, 1000, 3, [0, 9, 0, 0, self.gripper_force, self.gripper_v], 9)
        time.sleep(wait_time)

    def gripper_open(self):
        """
        夹爪开启
        """
        # 打开夹爪
        self.arm.Write_Registers(1, 1000, 3, [0, 9, 255, 0, self.gripper_force, self.gripper_v], 9)

    def get_data(self):
        """
        获取夹爪开合程度
        """
        # 获取夹爪的开合程度
        register_data = self.arm.Read_Multiple_Holding_Registers(1, 2000, 6, 9)
        gripper_status = int(bin(register_data[1][2])[2:].zfill(8)[:2], 2)
        hex_status = format(gripper_status, '08x')[-1]
        return hex_status
