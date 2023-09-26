import shutil

from scapy.all import *
import csv
import os, sys

from scapy.layers.inet import TCP, UDP


def getall(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            data.append(row)
        return data


def getlast(filepath):
    with open(filepath, 'r') as csvfile:
        reader1 = csv.reader(csvfile)
        # 遍历reader，获取最后一行
        for row in reader1:
            pass
        # 获取最后一行的第二个数据的值
        valuelast = row[1]
    return valuelast


def is_analysis(filepath):
    with open(filepath, 'r') as csvfile:
        reader1 = csv.reader(csvfile)
        # 遍历reader，获取最后一行
        row0 = next(reader1)
        # 获取最后一行的第二个数据的值
        valuelast = getlast(filepath)
        if (float)(valuelast) - (float)(row0[1]) > 60:
            return True
    return False


def read_csv1(filepath):
    data = getall(filepath)
    valuelast = getlast(filepath)
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        t_start = None
        l_first = None
        state = "s_0"
        row0 = None
        row1 = None
        row2 = None
        row3 = None
        row4 = None
        row5 = None
        a_t = None
        count = 0
        i_mid = 0
        firsta_t = 0
        for i in range(len(data)):
            for row in reader:
                i += 1
                if a_t != None:
                    if float(row[1]) - float(a_t) < 88:
                        continue
                if row[7] == "92" and state == "s_0":
                    l_first = row
                    t_start = float(row[1])
                    row0 = row
                    state = "s_1"
                    i_mid = i
                elif state == "s_1":
                    t_now = float(row[1])
                    if t_now - t_start <= 1.5:
                        if row[7] == "54":
                            if row[3] == l_first[4] and row[4] == l_first[3]:
                                state = "s_2"
                                row1 = row
                        else:
                            continue
                    else:
                        state = "s_0"
                elif state == "s_2":
                    t_now = float(row[1])
                    if t_now - t_start <= 1.5:
                        if int(row[7]) in range(240, 250) or row[7] in range(288, 310) or row[7] in range(338, 350):
                            if row[3] == l_first[4] and row[4] == l_first[3]:
                                state = "s_3"
                                row2 = row
                        else:
                            continue
                    else:
                        state = "s_0"
                elif state == "s_3":
                    t_now = float(row[1])
                    if t_now - t_start < 1.5:
                        if row[7] == "54" and row[3] == l_first[3] and row[4] == l_first[4]:
                            row3 = row
                            start_value = data[i_mid][1]
                            for k in range(i_mid, -1, -1):
                                current_value = data[k][1]
                                if abs(float(current_value) - float(start_value)) < 1.5:
                                    if data[k][7] == "54" and data[k][3] == l_first[4] and data[k][4] == l_first[3]:
                                        row4 = data[k]
                                        for j in range(k - 1, -1, -1):
                                            diff = abs(float(data[j][1]) - float(start_value))
                                            if diff < 1.5:
                                                if (int(data[j][7]) in range(450, 520) or int(data[j][7]) in range(
                                                        550, 700) or int(data[j][7]) in range(870, 890) or int(
                                                    data[j][7]) in range(910, 930)) and data[j][3] == l_first[3] and \
                                                        data[j][4] == l_first[4]:
                                                    row5 = data[j]
                                                    a_t = (float(row0[1]) + float(row1[1]) + float(row2[1]) + float(
                                                        row3[1]) + float(row4[1]) + float(row5[1])) / 6
                                                    if firsta_t == 0:
                                                        firsta_t = a_t
                                                    # print(str(row0) + "\n" + str(row1) + "\n" + str(row2) + "\n" + str(
                                                    #     row3) + "\n" + str(row4) + "\n" + str(row5) + "\n")
                                                    state = "s_0"
                                                    count += 1
                                                    break
                                            else:
                                                state = "s_0"
                                                break
                                            continue
                                else:
                                    state = "s_0"
                                    break
                            state = "s_0"
                            continue
                        else:
                            continue
                    else:
                        state = "s_0"
                else:
                    state = "s_0"
    alltime = (int)(((float)(valuelast) - firsta_t) // 90) - 1
    if alltime < 1:
        alltime = 1
    acc = count / alltime
    # print("accurancy：" + str(acc))
    return acc


def read_csv(filepath):
    with open(filepath, 'r') as csvfile:
        valuelast = getlast(filepath)
        count = 0
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        t_start = None
        l_first = None
        state = "s_0"
        row0 = None
        row1 = None
        row2 = None
        firsta_t = 0
        a_t = None
        for row in reader:
            if a_t != None:
                if float(row[1]) - float(a_t) < 18:
                    continue
            if row[7] == "100" and state == "s_0":
                l_first = row
                t_start = float(row[1])
                row0 = row
                state = "s_1"
            elif state == "s_1":
                t_now = float(row[1])
                if t_now - t_start <= 1.5:
                    if row[7] == "54":
                        if row[3] == l_first[4] and row[4] == l_first[3]:
                            state = "s_2"
                            row1 = row
                    else:
                        continue
                else:
                    state = "s_0"
            elif state == "s_2":
                t_now = float(row[1])
                if t_now - t_start <= 1.5:
                    if row[7] == "100":
                        if row[3] == l_first[4] and row[4] == l_first[3]:
                            state = "s_3"
                            row2 = row
                    else:
                        continue
                else:
                    state = "s_0"
            elif state == "s_3":
                t_now = float(row[1])
                if t_now - t_start <= 1.5:
                    if row[7] == "54":
                        if row[3] == l_first[3] and row[4] == l_first[4]:
                            a_t = (float(row0[1]) + float(row1[1]) + float(row2[1]) + float(row[1])) / 4
                            if firsta_t == 0:
                                firsta_t = a_t
                            row3 = row
                            # print(str(row0) + "\n" + str(row1) + "\n" + str(row2) + "\n" + str(row3) + "\n")
                            count += 1
                            state = "s_0"
                        else:
                            continue
                    else:
                        continue
                else:
                    state = "s_0"
        alltime = (int)(((float)(valuelast) - firsta_t) // 20) - 1
        if alltime < 1:
            alltime = 1
        acc = count / alltime
        # print("accurancy：" + str(acc))
        return acc


def pcap2csv(pcap_path, csv_path):
    # 打开 pcap 文件
    pcap = rdpcap("./toanalysis/"+pcap_path)
    # 获取第一个数据包的时间戳
    first_pkt_time = float(pcap[0].time)
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # 遍历每个数据包并提取信息
        for i, pkt in enumerate(pcap):
            # 获取时间和协议名称
            rel_time = str(float(pkt.time - first_pkt_time))
            proto = pkt.summary().split()[0]

            # 获取源 IP 和目标 IP
            if IP in pkt:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
            else:
                src_ip = "N/A"
                dst_ip = "N/A"

            # 获取源端口号和目标端口号
            if TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
            elif UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
            else:
                src_port = "N/A"
                dst_port = "N/A"

            # 获取包长
            length = len(pkt)
            # 写入一行数据
            writer.writerow([i + 1, rel_time, proto, src_ip, dst_ip, src_port, dst_port, length])


def read_file(file_name):
    dic_session = {}
    with open(file_name, 'r') as f:
        if file_name == "output.csv":
            for line in f:
                temp = line.split(',')
                pro = temp[2]
                src = temp[3]
                dst = temp[4]
                sport = temp[5]
                dport = temp[6]
                key1 = str(pro) + "_" + str(src) + "_" + str(sport) + "_" + str(dst) + "_" + str(dport)
                key2 = str(pro) + "_" + str(dst) + "_" + str(dport) + "_" + str(src) + "_" + str(sport)
                if key1 not in dic_session and key2 not in dic_session:
                    dic_session[key1] = []
                    dic_session[key1].append(line)
                else:
                    if key1 in dic_session:
                        dic_session[key1].append(line)
                    else:
                        dic_session[key2].append(line)
            for key in dic_session:
                if "N/A" in key:
                    continue
                else:
                    file = open("./tempfiles/" + file_name + "_" + key + ".csv", "w")
                    for line in dic_session[key]:
                        file.write(line)
                    file.close()


def heartbeat_analysis():
    pcap_file = "complextwitter.pcap"
    csv_file = "output.csv"
    pcap2csv(pcap_file, csv_file)
    read_file(csv_file)
    filelist = os.listdir('./tempfiles/')
    for file in filelist:
        if "csv" in file:
            filename='./tempfiles/'+file
            if is_analysis(filename):
                result0 = read_csv(filename)
                result1 = read_csv1(filename)
                acc = result1 + result0
                if acc > 1.2:
                    print(file + ":" + str(acc))
                    print("using twitter!")
                    shutil.copy(filename, "./result/"+file)
            os.remove(filename)
    os.remove(csv_file)


if __name__ == "__main__":
    heartbeat_analysis()
