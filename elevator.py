# Elevator system
# Logger class prints to stdout
# Elevator class offers methods to control the elevator
# Controller class has floor information, processes floor stop using FIFO
#    as well as stopping in the stops on the way to dst stop
class Logger:
    def info(self, msg: str):
        print(msg)
class Elevator:
    def __init__(self, max_weight: int, logger: Logger):
        self.curr_weight = 0
        self.max_weight = max_weight
        self.logger = logger
    def open_doors(self):
        self.logger.info("Open doors ...")
    def close_doors(self):
        self.logger.info("Close doors ...")
    def move_up(self):
        self.logger.info("Move up ...")
    def move_down(self):
        self.logger.info("Move down ...")
    def weight_ok(self) -> bool:
        self.logger.info("Weight is ok ...")
        return True
    def wait_for_people(self):
        self.open_doors()
        self.wait()
        self.close_doors()
    def wait(self):
        self.logger.info("Wait ...")
class Controller:
    def __init__(self, elevator: Elevator, nb_of_floors: int, logger: Logger):
        self.floors = [False for _ in range(nb_of_floors)]
        self.req = []
        self.curr_floor = 0
        self.dst_floor = 0
        self.elevator = elevator
        self.logger = logger
    # floors are indices and will be between 0 and n
    def go_to_floor(self, floor: int):
        if floor < 0 or floor >= len(self.floors):
            raise ValueError("Wrong request")
        self.floors[floor] = True
        self.req.append(floor)
        if self.dst_floor == floor:
            self._arrived_in_floor(floor)
        if self.dst_floor == -1:
            self.dst_floor = floor
        else:
            self.floors[floor] = True
            self.req.append(floor)
    def _arrived_in_floor(self, floor: int):
            if not self.floors[floor]:
                return None
            self.elevator.wait_for_people()
            while not self.elevator.weight_ok():
                self.elevator.wait_for_people()
            self.floors[floor] = False
            self.req = [x for x in self.req if x != floor]
            if self.dst_floor == floor:
                self.dst_floor = -1
    # moves elevator if there is a dst floor or pending requests
    def move_elevator(self):
        if self.dst_floor == self.curr_floor:
            self._arrived_in_floor(self.dst_floor)
            self.dst_floor = -1
            return False
        if self.dst_floor == -1 and not self.req:
            self.logger.info("Elevator idle ...")
            return False        
        if self.dst_floor == -1 and self.req:
            self.dst_floor = self.req[0]
        inc = -1 if self.dst_floor < self.curr_floor else 1
        self.curr_floor += inc
        if inc == 1:
            self.elevator.move_up()
        else:
            self.elevator.move_down()
        self.logger.info(f'floor: {self.curr_floor}')
        self._arrived_in_floor(self.curr_floor)
        return True
logger = Logger()
elevator = Elevator(100, logger)
controller = Controller(elevator, 10, logger)
controller.go_to_floor(2)
controller.move_elevator()
controller.move_elevator()
controller.move_elevator()

controller.go_to_floor(3)
controller.move_elevator()
controller.move_elevator()

controller.go_to_floor(1)
controller.move_elevator()
controller.move_elevator()

controller.go_to_floor(4)
controller.move_elevator()
controller.move_elevator()
controller.move_elevator()


controller.go_to_floor(2)
controller.move_elevator()
controller.move_elevator()
controller.move_elevator()
controller.move_elevator()
controller.move_elevator()

