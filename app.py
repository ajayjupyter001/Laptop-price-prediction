import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time

model = pickle.load(open("final_pipe.pkl","rb"))
df = pickle.load(open("df.pkl","rb"))
df_reso = pickle.load(open("df_reso.pkl","rb"))
st.image("laptops.jpg")
st.title("Laptop Price Prediction")

def get_resolution(df):
    final = []
    for i, j in zip(df["x_resol"], df["y_resol"]):
        final.append("{} x {}".format(i, j))
    return list(set(final))

company = st.selectbox(
    "Company",
     sorted(df["Company"].unique())
)

type = st.selectbox(
    "Type",
    sorted(df["TypeName"].unique())
)

ram = st.selectbox(
    "Ram",
    sorted(df["Ram"].unique())
)

opsys = st.selectbox(
    "OpSys",
    sorted(df["OpSys"].unique())
)

inches = st.number_input("Inches")
weight = st.number_input("Weight(in grams)")

touch = st.selectbox(
    "TouchScreen",
    ["Yes","No"]
)

ips = st.selectbox(
    "IPS",
    ["Yes","No"]
)

resolution = st.selectbox(
    "Resolution",
    get_resolution(df_reso)
)

cpu_type = st.selectbox(
    "CPU Brand",
    sorted(df["CPU_type"].unique())
)

ssd = st.selectbox(
    "SSD",
    sorted(df["SSD"].unique())
)

hdd = st.selectbox(
    "HDD",
    sorted(df["HDD"].unique())
)

gpu = st.selectbox(
    "GPU",
    sorted(df["GPU_brand"].unique())
)

gpu_brand = st.selectbox(
    "GPU brand",
    sorted(df[df["GPU_brand"] == gpu]["GPU_brand_types"].unique())
)

if st.button("Predict"):
    placeholder = st.empty()
    with placeholder.container():
        st.write("Gathering info......")


    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.019)
        my_bar.progress(percent_complete + 1)
    my_bar.empty()
    placeholder.empty()

    with placeholder.container():
        st.write("✔️ Successfully Gathered info")

    with st.spinner('Please Wait...'):
        time.sleep(5)
    x_res = int(resolution.split("x")[0])
    y_res = int(resolution.split("x")[1])

    if(touch == "Yes"):
         touch = 1
    else:
         touch = 0

    if (ips == "Yes"):
        ips = 1
    else:
        ips = 0


    ppi = (((x_res ** 2) + (y_res ** 2)) ** 0.5) / (inches+0.001)
    data = pd.DataFrame([[company, type, ram,opsys,weight,touch,ips,ppi,cpu_type,ssd,hdd,gpu,
                          gpu_brand]]).rename(columns={
        0: "Company", 1: 'TypeName', 2: 'Ram', 3: 'OpSys', 4: 'Weight', 5: 'Touchscreen', 6: 'Ips',
        7: 'Ppi', 8: 'CPU_type', 9: 'SSD', 10: 'HDD', 11: 'GPU_brand', 12: 'GPU_brand_types'
    })

    st.header("Overview Of Selected Features:")
    list_columns = list(data.columns)
    list_columns.insert(4,"Inches")
    list_columns.remove("Ppi")
    list_columns[1] = "Type"
    list_columns[8] = "CPU"
    list_columns[11] = "GPU"
    list_columns[12] = "GPU Type"
    list_columns.insert(8, "Resolution")
    list_values  = list(data.iloc[0,:])
    if (touch == 1):
        list_values[5]="Yes"
    else:
        list_values[5] = "No"

    if (ips == 1):
        list_values[6] = "Yes"
    else:
        list_values[6] = "No"

    list_values.insert(4,inches)
    list_values.remove(ppi)
    list_values.insert(8, resolution)

    display = pd.DataFrame({
        "Selected Feature":list_columns,
        "Selected Feature value":list_values
    })
    display = display.astype(str)
    st.table(display)
    st.title("The Predicted Price :")
    st.title(float("{0:.2f}".format(np.exp(model.predict(data)[0])).format(np.exp(model.predict(data))[0])))
    st.success('Done!')

