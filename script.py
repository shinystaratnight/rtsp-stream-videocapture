import cv2
import csv
import time
import calendar

# This is csv file name which contains IP list and port number
csv_filename = 'shodan_data.csv'

csv_output_filename = 'result'

result = [['IP', 'Stream Path', 'Image Name', 'Status']]
with open(csv_filename, 'r') as csvfile:
    reader = csv.reader(csvfile, skipinitialspace=True)
    next(reader)
    for row in reader:
        path_list = []
        path_list.append('rtsp://admin:admin@' + row[0] + ':' + row[1] + '/1/')
        path_list.append('rtsp://user:user@' + row[0] + ':' + row[1] + '/1/')
        path_list.append('rtsp://' + row[0] + ':' + row[1] + '/1/')

        image_path = ""
        status = "Not Working"
        stream_path = ''
        for i in range(3):
            vcap = cv2.VideoCapture(path_list[i])
            vcap.set(cv2.CAP_PROP_POS_MSEC, 0)
            ret, frame = vcap.read()

            if ret:
                image_path = row[0] + '.jpg'
                cv2.imwrite(image_path, frame)
                stream_path = path_list[i]
                status = ""
                break

        result.append([row[0], stream_path, image_path, status])

csv_output_filename = csv_output_filename + "_" + str(calendar.timegm(time.gmtime())) + ".csv"
with open(csv_output_filename, 'w') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(result)