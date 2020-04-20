import cv2
import csv
import time
import datetime
import calendar
from multiprocessing import Process, Array

ip_list = []
current_process_no = 0
result = [['IP', 'Image Name', 'Status']]
number_of_processes = 10
processes = []
ret_list = []


def read_csv():
    # This is csv file name which contains IP list and port number
    csv_filename = 'shodan_data_1.csv'
    # Get the list of IP and ports
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)
        next(reader)
        for row in reader:
            ip_list.append([row[0], row[1]])


def rtsp_reader_func(process_no, url, ret_list):
    rtsp_url = url + '/1/'
    path_list = ['rtsp://admin:admin@' + rtsp_url, 'rtsp://user:user@' + rtsp_url]
    print('Detecting IP Address : ', ip_list[process_no][0])

    for i in range(2):
        vcap = cv2.VideoCapture(path_list[i])
        vcap.set(cv2.CAP_PROP_POS_MSEC, 0)
        ret, frame = vcap.read()
        if ret:
            image_name = url.split(':')[0]
            image_path = image_name + '.jpg'
            cv2.imwrite(image_path, frame)
            ret_list[process_no] = 1
            break
    print("Process ", process_no, " finishes at ", datetime.datetime.now())


if __name__ == "__main__":
    read_csv()
    total_number_of_ips = len(ip_list)
    ret_list = Array('i', range(total_number_of_ips))
    while True:
        no_of_pending_process = 0
        for proc_container in processes:
            index = proc_container[2]
            if proc_container[0].is_alive():
                current_time = datetime.datetime.now()
                if (current_time - proc_container[1]).seconds >= 20:
                    print("Killing Process ", index)
                    proc_container[0].kill()
                    processes.remove(proc_container)
                    result.append([ip_list[index][0], "", "Not Working"])
                no_of_pending_process += 1
            else:
                proc_container[0].join()
                print("Removing Process ", index)
                processes.remove(proc_container)
                result.append([ip_list[index][0], ip_list[index][0] + ".jpg", ""])

        for i in range(number_of_processes - no_of_pending_process):
            if current_process_no < total_number_of_ips:
                proc = Process(target=rtsp_reader_func, args=(current_process_no, ip_list[current_process_no][0] + ":" + ip_list[current_process_no][1], ret_list))
                start_time = datetime.datetime.now()
                processes.append([proc, start_time, current_process_no])
                print("Process ", current_process_no, " starts at ", start_time)
                proc.start()
                current_process_no += 1

        time.sleep(0.5)

        if (len(processes) == 0):
            break

    for index, ret in enumerate(ret_list):
        if ret != 1:
            result[index + 1][1] = ""
            result[index + 1][2] = "Not Working"
    # Write the results into csv file
    csv_output_filename = 'result' + "_" + str(calendar.timegm(time.gmtime())) + ".csv"
    with open(csv_output_filename, 'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(result)