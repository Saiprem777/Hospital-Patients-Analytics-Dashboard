import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

df= pd.read_csv(r"D:\vs\hospital_patient_data_100_rows.csv")
df["Admission_Date"]=pd.to_datetime(df["Admission_Date"])
df.loc[df["Gender"] == "Other", "Gender"] = np.random.choice(["Male", "Female"], size=(df["Gender"] == "Other").sum())


illness_counts = df["Illness"].value_counts().reset_index()
illness_counts.columns = ["Illness", "Count"]
illness_counts = illness_counts.sort_values("Count", ascending=False)

fig1 = px.bar(
    illness_counts, x="Illness", y="Count", color="Illness",
    title="Top Illnesses in Patients", text="Count"
)

fig1.update_layout(
    title_font_size=22,
    xaxis_title="Illness",
    yaxis_title="Patient Count",
    xaxis_tickangle=-30,
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14),
    showlegend=False
)

fig1.update_traces(
    texttemplate='%{text}', textposition='outside'
)
gender_counts = df["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]
fig2 = px.pie(
    gender_counts,
    names="Gender",
    values="Count",
    title="Gender Distribution of Patients",
    color="Gender",  
    color_discrete_map={
        "Male": "#1f77b4",
        "Female": "#ff6347",
        "Other": "#9b59b6"    
    },
    hole=0.3
)
fig2.update_traces(
    textinfo='percent+label',
    textfont_size=14,
    pull=[0.05 if g == "Female" else 0 for g in gender_counts["Gender"]]
)

fig2.update_layout(
    showlegend=True,
    legend_title_text='Gender',
    title_font_size=20
)
median_order = df.groupby("Illness")["Treatment_Cost"].median().sort_values(ascending=False).index
fig3 = px.box(
    df,
    x="Illness",
    y="Treatment_Cost",
    color="Illness",
    title="Treatment Cost Distribution by Illness",
    category_orders={"Illness": median_order},
    points="all",
    hover_data=["Name", "Age", "Gender", "Admission_Date"]
)
fig3.update_layout(
    xaxis_title="Illness Type",
    yaxis_title="Treatment Cost (₹)",
    title_font_size=20,
    font=dict(size=13),
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)"
)
fig3.update_traces(marker=dict(opacity=0.5), jitter=0.3)
monthly_admissions = df["Admission_Date"].dt.to_period("M").value_counts().sort_index()
monthly_df = monthly_admissions.reset_index()
monthly_df.columns = ["Month", "Admissions"]
monthly_df["Month"] = monthly_df["Month"].astype(str)

fig4 = px.line(
    monthly_df,
    x="Month",
    y="Admissions",
    title="Monthly Patient Admissions Over Time",
    markers=True,
    text="Admissions"
)
fig4.update_traces(textposition="top center", line=dict(color="#0077b6", width=3))

fig4.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Admissions",
    xaxis_tickangle=-45,
    title_font_size=20,
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(size=13),
    hovermode="x unified",
    margin=dict(t=60, b=80)
)
fig4.update_xaxes(type="category")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🏥 Hospital Patient Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4)


])

if __name__ == '__main__':
    app.run(debug=True)

