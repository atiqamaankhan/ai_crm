# analytics.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

def attendance_dummy_report(csv_path="attendance_sample.csv", out_folder="static/plots"):
    os.makedirs(out_folder, exist_ok=True)
    # If file missing, create a tiny sample
    if not os.path.exists(csv_path):
        # sample attendance: name, date, time, status
        df = pd.DataFrame({
            "name": ["Alice","Bob","Charlie","Alice","Bob"],
            "date": ["2025-09-01","2025-09-01","2025-09-01","2025-09-02","2025-09-02"],
            "status": ["Present","Absent","Present","Present","Present"]
        })
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)
    # Simple counts
    counts = df.groupby("name")["status"].apply(lambda s: (s=="Present").sum()).reset_index(name="present_count")
    plt.figure(figsize=(6,4))
    sns.barplot(data=counts, x="name", y="present_count")
    plt.title("Present Counts per Student (sample)")
    out = os.path.join(out_folder, "attendance_counts.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("Saved plot to", out)
    return out
