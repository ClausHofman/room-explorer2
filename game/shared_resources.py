import threading

# Initialize stop_event
stop_event = threading.Event()




# Notes on a singleton approach
# import threading

# class SharedResources:
#     _stop_event = None

#     @staticmethod
#     def get_stop_event():
#         if SharedResources._stop_event is None:
#             SharedResources._stop_event = threading.Event()
#         return SharedResources._stop_event

# from shared import SharedResources

# stop_event = SharedResources.get_stop_event()

# from shared import SharedResources

# stop_event = SharedResources.get_stop_event()
