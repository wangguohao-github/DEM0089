import pandas as pd
import numpy as np
import datetime
import math

def sample_generate_for_dl(excel_name,sheet_names,column_names,window_seconds,window_overlapping):
    sample_hz = 50 #传感器采样频率
    window_size=int(window_seconds*sample_hz) #window_size是一个样本包含的data points
    sample_num_fre=int(window_size/2)
    # writer1=pd.ExcelWriter("data_for_dl_"+excel_name+"_"+str(window_seconds)+".xlsx",engine='openpyxl')
    df_total=pd.DataFrame()

    for sheet_name in sheet_names:  #sheet是标签类别
        print(excel_name+"_"+sheet_name+"开始")
        starttime = datetime.datetime.now()
        df=pd.read_excel(excel_name, sheet_name=sheet_name.split(".")[0],index_col=None,header=0)
        df_sheet=pd.DataFrame()
        i = 0
        while i-df.shape[0]< 0 : #遍历数据
            if i+window_size-df.shape[0]< 0: #该样本序列最后一条数据也在dataframe维度之内
                if (abs(int(df["time"][i+window_size-1])-int(df["time"][i]))/1000000000) < 2*window_seconds:
                    # for j in range(window_size):#判断数据是否是连续的
                    df_sheet=pd.concat([df_sheet,df.loc[i:i+window_size-1,column_names]],axis=0)
                    i = i + int(window_size * (1 - window_overlapping))
                else:
                    i = i + 1
            else:#如果该样本最后一条数据已经超出dataframe大小，那么删除掉最后这个样本的剩余数据
                # for j in range(i,df.shape[0]):
                #     df.drop([i], inplace=True)
                #     df=df.reset_index(drop=True)
                break
        df_total=pd.concat([df_total,df_sheet],axis=0)
        endtime = datetime.datetime.now()

        print(excel_name + "_" + sheet_name + "结束，耗时")
        print(endtime - starttime)

    print("正在写入"+excel_name)
    # df_total.to_excel(excel_writer=writer1, sheet_name="time_domain",encoding="utf-8", index=False, header=True,engine='openpyxl')
    df_total.to_csv("data_for_dl_"+excel_name+"_"+str(window_seconds)+".csv",header=True)

if __name__ == "__main__":

    sheet_names = ["1", "2","3", "4","5", "6","7", "8"]
    column_names = ["Label", "x", "y", "z"]
    excel_names = ["test.xlsx"]

    seconds = [0.5,1,1.5,2]
    for excel_name in excel_names:
        for second in seconds:
            print("开始时间窗口为" + str(second) + "s的" + excel_name)
            starttime = datetime.datetime.now()  # 记录程序运行时间
            sample_generate_for_dl(excel_name, sheet_names, column_names, second, 0.5)
            endtime = datetime.datetime.now()
            print(endtime - starttime)