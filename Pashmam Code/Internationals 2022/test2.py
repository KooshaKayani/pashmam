# from multiprocessing import Process
# import cv2
# import requests

# def func_run_forever():
#     cap = cv2.VideoCapture(0)
#     while(True):
#         ret, frame = cap.read()
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# def func_run_once():
#     res = requests.get('https://www.google.com.au')
#     print(res)

# if __name__ == '__main__':
#     p1 = Process(target=func_run_forever)
#     p2 = Process(target=func_run_once)
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
# import multiprocessing


# def worker(procnum, return_dict):
#     print(str(procnum) + " represent!")
#     return_dict[procnum] = procnum


# if __name__ == "__main__":
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i, return_dict))
#         jobs.append(p)
#         p.start()

#     for proc in jobs:
#         proc.join()
#     print(return_dict.values())
#!/usr/bin/env python